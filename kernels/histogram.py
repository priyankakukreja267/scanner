import tensorflow as tf
import numpy as np
from src.kernel import Kernel
from PIL import Image
import cv2


class HistogramKernel(Kernel):
    """
    For now this is in python, which sucks.
    """
    def __init__(self, flag='pil'):
        self.flag = flag

    def apply(self, inputs):
        def pil_histogram(image):
            return np.asarray(Image.fromarray(image).histogram())

        def opencv_histogram(image):
            return cv2.calcHist(image, [0], None, [256], [0,256])

        if self.flag is 'pil':
            return [tf.py_func(pil_histogram, [inputs[0]], [tf.int64])]
        else:
            return [tf.py_func(opencv_histogram, [inputs[0]], [tf.int64])]

    def get_input_dtypes(self):
        return [np.dtype('uint8')]

    def get_output_dtypes(self):
        return [(False, np.dtype('int64'))]

    def reset(self):
        pass
