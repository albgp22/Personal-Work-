from SlidingWindow import SlidingWindow, Rectangle, plot_rectangle
import constants as C

import numpy as np
import cv2


def to_face_ratio(config):
    config = np.asarray(config, dtype='object')

    for i in range(len(config)):
        assert(isinstance(config[i][0], float))
        config[i][0] = (config[i][0], C.FACE_WIDTH_WRT_HEIGHT_RATIO * config[i][0])

    return config


# Class that detects a face of a SINGLE image using the sliding window method with different sizes
class FaceDetector(object):
    def __init__(self, model, image):
        self.model = model
        self.image = image
        self.iteration = 0

        self.main_rectangle = Rectangle.create((0,0), image.shape[1], image.shape[2]).round()
        self.history = [[self.main_rectangle, self.predict(self.main_rectangle)]]
        self.deformation = C.MINIMUM_DEFORMATION * self.main_rectangle[1:3]

        assert self.main_rectangle.big_enough(), "Image too small!"

    def change_image(self, new_image, new_rectangle, debug=0):
        assert self.image.shape == new_image.shape

        self.image = new_image
        pred = self.predict(new_rectangle)

        self.update_parameters(new_rectangle, pred)

    def detect_impl(self, config, is_face, debug=0):
        config = np.asarray(config, dtype='object')

        rects = []
        for rect_dims_perc, stride_perc in config:
            sw = SlidingWindow(self.model, self.image, rect_dims_perc, stride_perc, self.history[self.iteration][0])
            rectangle = sw.apply(is_face, debug=debug)

            if rectangle is not None and rectangle.big_enough():
                rects.append(rectangle)

        return Rectangle.from_array(np.asarray(rects).mean(0)).round() if len(rects) > 0 else None

    def detect_single(self, debug=0):
        new_rectangle = self.detect_impl(to_face_ratio(C.DETECT_SETTINGS), lambda pred: pred[1] > pred[0], debug=debug)

        if new_rectangle is not None:
            prediction = self.predict(new_rectangle)
            prev_rect, prev_pred = self.history[self.iteration]

            if debug > 0:
                print("Found a rectangle {}".format(new_rectangle))
                plot_rectangle(self.image, new_rectangle, self.history[self.iteration][0],
                               "Iteration {} ({}%)".format(self.iteration, int(prediction*100)))

            if (prediction + C.FACE_LOST_TRACK_EPSILON < prev_pred or prediction < 0.5) and prev_pred > 0.5:
                if debug > 0:
                    print("It seems to be the wrong path")

                # Calculate the direction to reduce the old rectangle
                dir_y, dir_x = self.deformation
                if prev_rect.center()[0] < new_rectangle.center()[0]:
                    dir_y = -dir_y
                if prev_rect.center()[1] < new_rectangle.center()[1]:
                    dir_x = -dir_x

                if debug > 0:
                    print("DIR ", (dir_y, dir_x))
                    plot_rectangle(self.image, prev_rect, self.history[max(0, self.iteration-1)][0], "Going back ({}%)".format(int(prev_pred*100)))
                    print("1 -> ", prev_rect)

                new_rectangle = prev_rect.expand((dir_y, dir_x), self.main_rectangle)
                if debug > 0:
                    plot_rectangle(self.image, new_rectangle, self.history[max(0, self.iteration-1)][0], "Expanded ({}%)".format(-1))

                if debug > 0:
                    print("2 -> ", new_rectangle)
                new_rectangle = new_rectangle.reduce((dir_y, dir_x))

                prediction = self.predict(new_rectangle)
                if debug > 0:
                    print("3 -> ", new_rectangle)
                    plot_rectangle(self.image, new_rectangle, self.history[max(0, self.iteration-1)][0], "Reduced ({}%)".format(int(prediction*100)))

                self.iteration -= 1
        else:
            if debug > 0:
                print("Lost rectangle, expanding...")

            rect, prob = self.history[self.iteration]

            if debug > 0:
                plot_rectangle(self.image, rect, self.history[max(0, self.iteration-1)][0], "Previous one ({}%)".format(int(prob*100)))
                print("1 --> ", rect)

            new_rectangle = rect.expand(self.deformation, self.main_rectangle).expand(-self.deformation, self.main_rectangle)
            prediction = self.predict(new_rectangle)

            if debug > 0:
                plot_rectangle(self.image, new_rectangle, self.history[max(0, self.iteration-1)][0], "Expanded ({}%)".format(int(prediction*100)))
                print("2 --> ", new_rectangle)

            self.iteration -= 1

        self.update_parameters(new_rectangle, prediction)

    def detect(self, max_iterations=C.MAX_DETECT_ITERATIONS, debug=0):
        assert max_iterations >= 0

        if debug > 0:
            plot_rectangle(self.image, self.history[self.iteration][0], self.main_rectangle, "Beginning ({}%)".format(int(self.history[self.iteration][1] * 100)))

        self.detect_single(debug=debug)

        while not self.stop(debug=debug) and max_iterations > 0:
            self.detect_single(debug=debug)
            max_iterations -= 1

        rect, prob = self.history[self.iteration]
        if debug > 0:
            plot_rectangle(self.image, rect, self.main_rectangle, "Final ({}%)".format(int(prob*100)))

        return self.history[self.iteration]

    def detect_sequence(self, generator, max_iterations=C.MAX_DETECT_ITERATIONS, plot_iterations=False, debug=0):
        print("Processing first image...")
        new_rectangle, pred = self.detect(max_iterations, debug)
        prev_pred = pred

        solutions = [(new_rectangle, pred)]
        counter = 2

        while not generator.stop():
            print("Processing image number {}...".format(counter))
            if plot_iterations:
                plot_rectangle(self.image, new_rectangle, self.main_rectangle, title="Image {} ({}%)".format(counter-1, int(pred*100)))
            counter += 1

            new_image = generator.get()

            if pred < 0.5 or pred + C.FACE_LOST_TRACK_EPSILON < prev_pred:
                self.iteration = 0 # We can't reuse the previous work
                self.change_image(new_image, self.main_rectangle, debug=debug)
            else:
                if debug > 0:
                    print("1 -> ", new_rectangle)
                    plot_rectangle(self.image, new_rectangle, self.main_rectangle, title="Previous solution")

                new_rectangle = new_rectangle.expand(self.deformation, self.main_rectangle)
                new_rectangle = new_rectangle.expand(-self.deformation, self.main_rectangle)

                pred = self.predict(new_rectangle)
                if debug > 0:
                    print("2 -> ", new_rectangle)
                    plot_rectangle(self.image, new_rectangle, self.main_rectangle,
                                   title="Expanded previous solution ({}%)".format(int(pred*100)))

                self.change_image(new_image, new_rectangle, debug=debug)

            new_rectangle, pred = self.detect(max_iterations, debug)
            solutions.append((new_rectangle, pred))

        if plot_iterations:
            plot_rectangle(self.image, new_rectangle, self.main_rectangle,
                           title="Image {} ({}%)".format(counter - 1, int(pred*100)))

        return solutions

    def get_parameters(self):
        profundity = 1
        rect = self.history[self.iteration][0]

        return np.asarray((rect.center()[0], rect.center()[1], profundity))

    def predict(self, rectangle):
        subimage = self.image[:, rectangle[0][0]:rectangle[3][0], rectangle[0][1]:rectangle[3][1]].reshape(rectangle[1:3])
        subimage = cv2.resize(subimage, C.IMG_DIMS).reshape((1,1) + C.IMG_DIMS)

        return self.model.predict(subimage, 1)[0][1]

    def update_parameters(self, new_rectangle, prediction):
        self.iteration += 1

        if self.iteration == len(self.history):
            self.history.append([new_rectangle, prediction])
        else:
            self.history[self.iteration] = (new_rectangle, self.predict(new_rectangle))

    def stop(self, debug=0):
        rect, prediction = self.history[self.iteration]

        if self.iteration == 0:
            prev_rect = self.main_rectangle
        else:
            prev_rect, _ = self.history[self.iteration - 1]

        ratio = rect.area() / prev_rect.area()

        if debug > 0 and prediction > C.IS_FACE_THRESHOLD:
            print("Stopping: Likely to be a face")
        if debug > 0 and self.iteration > 0 and ratio > C.STOP_RATIO_THRESHOLD:
            print("Stopping: Inner and outer rectangles are alike")

        return prediction > C.IS_FACE_THRESHOLD or (ratio > C.STOP_RATIO_THRESHOLD if self.iteration > 0 else ratio == 1)
