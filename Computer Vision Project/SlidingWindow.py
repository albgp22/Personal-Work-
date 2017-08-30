from plotting import plot_rectangle, plot_image
from utility import longest_connected_component, cartesian_product
import constants as C

import numpy as np
import cv2
import math


# Represent the rectangles that the sliding window generates
class Rectangle(np.ndarray):
    def __init__(self):
        super.__init__()

    @staticmethod
    def create(left_top_corner, height, width, right_bottom_corner=None):
        left_top_corner = np.asarray(left_top_corner, dtype='int32')
        if right_bottom_corner is None:
            right_bottom_corner = (left_top_corner + (height, width)).astype('int32')
        return np.asarray((left_top_corner, int(height), int(width), right_bottom_corner)).view(Rectangle)

    @staticmethod
    def from_array(args):
        assert args.shape[0] >= 3 and args[0].shape == (2,)
        return Rectangle.create(args[0], args[1], args[2])

    def big_enough(self):
        return (self[1:3] >= C.RECTANGLE_LOWER_BOUND_THRESHOLD).all()

    def area(self):
        return self[1] * self[2]

    def center(self):
        return self[0] + (self[1] // 2, self[2] // 2)

    def round(self):
        other = Rectangle.from_array(self)
        other[0] = other[0].astype('int32')
        other[1:3] = other[1:3].astype('int32')
        other[3] = other[0] + other[1:3]

        return other

    def expand(self, direction, outer):
        direction = np.asarray(direction)

        def expand_interval(dir, point, size, opoint, osize):
            if dir > 0:
                return point, min(size + dir, opoint + osize - point)
            else:
                new_point = max(opoint, point + dir)
                return new_point, size + point - new_point

        y, height = expand_interval(direction[0], self[0][0], self[1], outer[0][0], outer[1])
        x, width = expand_interval(direction[1], self[0][1], self[2], outer[0][1], outer[2])

        return Rectangle.create((y, x), height, width)

    def reduce(self, direction):
        direction = np.asarray(direction)

        def reduce_interval(dir, point, size):
            if dir > 0:
                new_point = point + min(dir, size)
                return new_point, size - (new_point - point)
            else:
                return point, max(0, size + dir)

        y, height = reduce_interval(direction[0], self[0][0], self[1])
        x, width = reduce_interval(direction[1], self[0][1], self[2])

        return Rectangle.create((y,x), height, width)


# Class that represent the mask applied to an image's section, i.e., which pixels of the image are predicted as
# part of a face
class Mask(object):
    def __init__(self, mask):
        self.mask = np.asarray(mask, 'int32')

    # Returns if there is any match in the current mask
    def any_match(self):
        return np.count_nonzero(self.mask) != 0

    # Try to clean up the predictions table and remove the outliers
    def clean(self):
        if self.mask.max() != 0:
            neighbors = cartesian_product([-1,0,1,0], [-1,0,1,0]) # 8-directions neighbors
            self.mask = longest_connected_component(self.mask, neighbors, lambda m, i, j: m[i][j] != 0)

    # Returns the center of the rectangle that arises from the current mask
    def get_centroid(self):
        coords = cartesian_product(np.arange(0, self.mask.shape[0]), np.arange(0, self.mask.shape[1]))
        non_zero_count = np.count_nonzero(self.mask)

        # Mean coordinates values after filtering the image with the mask
        return np.asarray([(coords[:,:,i] * self.mask).sum() / non_zero_count for i in (0,1)])

    # Return the size of the rectangle crossing centroid with direction axis_angle
    def get_diameter_single(self, centroid, axis_angle):

        # Returns the size of the semi-rect that starts at centroid with direction axis_angle
        def extend(angle):
            p0 = centroid.astype('int32')
            point = p0

            radius = 0
            prevradius = 0

            # While the current point is valid increase the radius by one
            while np.all(point >= 0) and np.all(point < self.mask.shape) and self.mask[point[0]][point[1]] != 0:
                prev = point
                prevradius = radius

                # While we don't change the current point
                while np.all(point >= 0) and np.all(point < self.mask.shape) and (point == prev).all():
                    radius += 1
                    point = np.round(p0 + (radius * math.cos(angle), radius * math.sin(angle))).astype('int32')

            # Getting the correct radius
            if radius > 0:
                radius = prevradius

            return radius

        # Radius of the semi-rects extending them towards both directions
        return np.asarray((extend(axis_angle), extend(math.pi + axis_angle)))

    def get_diameter(self, centroid, axis_angle, angle, num_lines, bound):
        ls = np.linspace(-angle/2, angle/2, num_lines) # All the angles we are going to check

        # Store all the diameters by the given angles
        diameters = np.floor(list(map(
            lambda alpha: self.get_diameter_single(centroid, math.radians(axis_angle + alpha)) * math.cos(math.radians(alpha)),
            ls
        )))

        assert (diameters.sum(1) <= bound).all()

        # Return its median (instead of the median to decrease the influence of outliers)
        return np.median(diameters, axis=0)

    def get_rectangle(self, begin=np.asarray((0,0))):
        centroid = self.get_centroid()
        height = self.get_diameter(centroid, 0, C.WIDTH_ANGLE, C.NUM_LINES, self.mask.shape[0])
        width = self.get_diameter(centroid, 90, C.HEIGHT_ANGLE, C.NUM_LINES, self.mask.shape[1])

        left_top_corner = begin + centroid - (height[1], width[1])

        return Rectangle.create(left_top_corner, height.sum() + 1, width.sum() + 1)


# Class that represents all the predictions done to an image in one slide
class Predictions(object):
    def __init__(self, predictions):
        self.preds = predictions

    def __getitem__(self, item):
        return self.preds.__getitem__(item)

    # Try to clean up the predictions table removing the outliers
    def clean(self):
        if self.preds.max() != 0:
            neighbors = ((0, 1), (1, 0), (0, -1), (-1, 0)) # 4-directions neighbors
            self.preds = longest_connected_component(self.preds, neighbors, lambda p, i, j: p[i][j] != 0)


# Represents the sliding process on an image section
class SlidingWindow(object):
    def __init__(self, model, image, rect_dims_perc, stride_perc, outer_rect):
        self.model = model
        self.image = image
        self.outer = outer_rect.round()
        self.image_size = self.outer[1:3]
        assert(self.image_size == self.outer[3] - self.outer[0]).all()

        self.rect_size = (np.minimum(1, rect_dims_perc) * self.image_size).astype('int32')
        self.step_size = (np.minimum(1, stride_perc) * self.rect_size).astype('int32')

        ys = np.arange(self.outer[0][0], self.outer[3][0] - self.rect_size[0], self.step_size[0], dtype='int32')
        xs = np.arange(self.outer[0][1], self.outer[3][1] - self.rect_size[1], self.step_size[1], dtype='int32')

        if len(ys) == 0:
            ys = np.zeros(1, dtype='int32')
        elif ys[-1] < self.outer[3][0] - self.rect_size[0]:
            ys = np.concatenate((ys, (self.outer[3][0] - self.rect_size[0],))).astype('int32')

        if len(xs) == 0:
            xs = np.zeros(1, dtype='int32')
        elif xs[-1] < self.outer[3][1] - self.rect_size[1]:
            xs = np.concatenate((xs, (self.outer[3][1] - self.rect_size[1],))).astype('int32')

        self.cartesian_product = cartesian_product(ys, xs)

        assert (self.outer[0] <= self.outer[3]).all()
        assert (self.rect_size <= self.image_size).all()
        assert (self.step_size <= self.image_size).all()

    def is_degenerated(self):
        return not Rectangle.create((0,0), self.rect_size[0], self.rect_size[1]).big_enough()

    # Do the sliding and for each one predicts if it's a face generating a predictions table
    def slide_and_predict(self, is_face):
        if self.is_degenerated():
            return None

        aux = self.cartesian_product.reshape((-1, 2))
        subimages = [cv2.resize(
            self.image[:, y:min(y + self.rect_size[0], self.outer[3][0]),
            x:min(x + self.rect_size[1], self.outer[3][1])].reshape(self.rect_size),
            C.IMG_DIMS) for y, x in aux]
        subimages = np.asarray(subimages).reshape((-1, 1) + C.IMG_DIMS)

        predictions = self.model.predict(subimages, batch_size=len(subimages))
        #predictions = np.apply_along_axis(is_face, 0, predictions).reshape(self.cartesian_product.shape[:-1])
        predictions = (predictions[:, 1] > predictions[:, 0]).reshape(self.cartesian_product.shape[:-1])
        return Predictions(predictions)

    # Returns the mask associated to the given predictions table
    def get_mask(self, predictions):
        if predictions is None:
            return None

        mask = np.zeros(self.image_size) # Initialize with zeros
        for i in range(self.cartesian_product.shape[0]):
            for j in range(self.cartesian_product.shape[1]):
                x, y = self.cartesian_product[i][j] - self.outer[0]

                # Increase the section by one
                if predictions[i][j]:
                    mask[x:x + self.rect_size[0], y:y + self.rect_size[1]] += 1

        if np.max(mask) > 0:
            mask = (mask != 0).astype('bool')
            #mask = (mask // np.max(mask)).astype('int32')
            #aux = mask != 0
            #mask[aux] = mask[aux] >= 2/3*mask[aux].mean()

        return Mask(mask)

    def apply(self, is_face, debug=0):
        if debug > 0:
            print("Sliding...")
        predictions = self.slide_and_predict(is_face)
        if predictions is None:
            return None

        if debug > 0:
            print("Cleaning...")

        if debug > 2:
            plot_image(predictions.preds)
            plot_image(self.get_mask(predictions).mask)

        predictions.clean()
        if debug > 0:
            print("Getting mask...")
        mask = self.get_mask(predictions)
        #mask.clean() # Way too slow

        if debug > 2:
            plot_image(predictions.preds)
            plot_image(mask.mask)

        if not mask.any_match():
            return None

        if debug > 0:
            print("Getting rectangle...")
        my_rectangle = mask.get_rectangle(self.outer[0])
        assert (my_rectangle[0] >= self.outer[0]).all() and (my_rectangle[3] <= self.outer[3]).all(), \
            "Rectangle out of bounds! {} {} {} {} ".format(
                self.outer[0], self.outer[3], my_rectangle[0], my_rectangle[3])

        if debug > 0:
            print("Done.")

        if debug > 1:
            print("HI")
            plot_rectangle(self.image, my_rectangle, self.outer)

        return my_rectangle
