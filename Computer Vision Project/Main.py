from FaceDetector import FaceDetector
from NeuralNetwork import NeuralNetwork
from SlidingWindow import plot_rectangle
import constants as C

import numpy as np
import time
import cv2


class Cam(object):
    def __init__(self):
        self.cam = cv2.VideoCapture(0)
        self.cam.set(cv2.CAP_PROP_FPS, C.CAM_FPS)
        self.current_image = None

    def get(self):
        if self.current_image is not None:
            return self.current_image

        image = cv2.imread('examples/frames/output193.jpg', 0)
        #_, image = self.cam.read()
        #cv2.imwrite('outputs/original.jpg', image)
        #image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        image = cv2.equalizeHist(image)
        image = image.reshape((1,) + image.shape) / C.NGRAYSCALE

        self.current_image = np.copy(image)
        return self.current_image

    def current(self):
        return self.current_image if self.current_image is not None else self.get()

    def stop(self):
        return False

    def dimensions(self):
        return self.current().shape[1:]
        #return self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT), self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)


class ImagesSequence(object):
    def __init__(self):
        self.current_image = None
        self.next = 77

    def get(self):
        name = "output{}".format("0{}".format(self.next) if self.next < 100 else self.next)
        image = cv2.imread('examples/frames/' + name + '.jpg', 0)
        image = cv2.equalizeHist(image)
        image = image.reshape((1,) + image.shape) / C.NGRAYSCALE

        self.current_image = np.copy(image)
        self.next += 1

        return self.current_image

    def stop(self):
        return self.next > 204

    def dimensions(self):
        return self.current_image.shape[1:]
        #return self.cam.get(cv2.CAP_PROP_FRAME_HEIGHT), self.cam.get(cv2.CAP_PROP_FRAME_WIDTH)


if __name__ == "__main__":
    model = NeuralNetwork().load('neural_network.h5')
    cam = ImagesSequence()
    detector = FaceDetector(model, cam.get())

    start = time.time()
    results = detector.detect_sequence(cam, plot_iterations=True, debug=0)
    rect, prob = results[-1]
    end = time.time()

    print("Done in ", end - start, " seconds")
    print("Probability of being a face: ", prob)
    if prob > 0.5:
        print("Found")
    else:
        print("Nothing was there")

    plot_rectangle(cam.current_image, rect, detector.main_rectangle, "Result")

    # model = NeuralNetwork().load('neural_network.h5')
    # start = time.time()
    # cam = Cam()
    # detector = FaceDetector(model, cam.get())
    #
    # start = time.time()
    # rect, prob = detector.detect(debug=1)
    # end = time.time()
    #
    # print("Done in ", end - start, " seconds")
    # print("Probability of being a face: ", prob)
    # if prob > 0.5:
    #     print("Found")
    # else:
    #     print("Nothing was there")
    #
    # plot_rectangle(cam.current_image, rect, detector.main_rectangle, "Result")
