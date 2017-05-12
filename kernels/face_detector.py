import tensorflow as tf
import numpy as np
from src.kernel import Kernel
import cv2


face_cascade = cv2.CascadeClassifier("data/haarcascade_frontalface_default.xml")
eye_cascade = cv2.CascadeClassifier("data/haarcascade_eye.xml")


class FaceDetectorKernel(Kernel):
    """
    """

    def apply(self, inputs):
        def face_detector(image):
            grayscale = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
            faces = face_cascade.detectMultiScale(grayscale, 1.3, 5)

            coords = []
            for (x, y, w, h) in faces:
                coords.extend([x, y, w, h])
            return np.asarray(coords, dtype='int64')

        return [tf.py_func(face_detector, [inputs[0]], [tf.int64])]

    def get_input_dtypes(self):
        return [np.dtype('uint8')]

    def get_output_dtypes(self):
        return [(False, np.dtype('int64'))]

    def reset(self):
        pass
