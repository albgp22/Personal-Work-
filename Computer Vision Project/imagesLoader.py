import constants as C

from math import ceil
import numpy as np
import os
import re
import cv2


# Helper function to load the images in batchs. Speeds up the process quite a lot.
def load_images_batch(path, pattern, max_size, size, left, right, discard=False):
    images = []
    for file in os.listdir(path)[left:right]:
        file = path + os.pathsep + file
        if not os.path.isdir(file):
            if pattern is not None:
                match = re.search(pattern, file)

            if pattern is None or (match is None if discard else match is not None):
                img = cv2.imread(file, 0)
                img = cv2.resize(img, C.IMG_DIMS, interpolation=cv2.INTER_AREA)
                img = img.reshape((1,) + C.IMG_DIMS) / C.NGRAYSCALE
                images.append(img)

                if max_size is not None and size >= max_size:
                    return np.asarray(images)

    return None if len(images) == 0 else np.asarray(images)


def load_images(path, pattern=None, max_depth=-1, depth=0, max_size=None, size=0, batch_size=1000, discard=False):
    if depth == max_depth:
        return None

    # Gets all the images from the current directory using batches
    images = None
    for i in range(0, len(os.listdir(path)), batch_size):
        aux = load_images_batch(path, pattern, max_size, size, i, i + batch_size, discard)
        if aux is not None:
            images = aux if images is None else np.concatenate((images, aux))
            size += aux.shape[0]

    # We need to know the number of directories to split up uniformly the number of images to load
    num_dirs = 0
    for file in os.listdir(path):
        file = path + os.pathsep + file
        if os.path.isdir(file):
            if pattern is not None:
                match = re.search(pattern, file)

            if pattern is None or (match is None if discard else match is not None):
                num_dirs += 1

    # Recursively we take images from the directories
    for file in os.listdir(path):
        file = path + os.pathsep + file

        if os.path.isdir(file):
            if pattern is not None:
                match = re.search(pattern, file)

            if pattern is None or (match and match.endpos == len(file)):
                aux = load_images(file, pattern, max_depth, depth + 1,
                                  None if max_size is None else ceil((max_size - size) / num_dirs), discard)
                if aux is not None:
                    images = aux if images is None else np.concatenate((images, aux))

    return None if images is None else (images[:max_size] if max_size is not None else images)


def get_samples(args):
    X, y = (None, None)

    for path, pattern, max_size_images, face, discard in args:
        print("Working with {}...".format(path))

        size = 0 if X is None else X.shape[0]
        samples = load_images(path, pattern, max_size=max_size_images - size, discard=discard)

        if samples is not None:
            if X is None:
                X = samples
                y = np.ones(samples.shape[0]) if face else np.zeros(samples.shape[0])
            else:
                X = np.concatenate((X, samples))
                y = np.concatenate((y, np.ones(samples.shape[0]) if face else np.zeros(samples.shape[0])))

    return X, y
