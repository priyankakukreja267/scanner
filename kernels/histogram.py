import tensorflow as tf
import numpy as np
from src.kernel import Kernel
from PIL import Image


class HistogramKernel(Kernel):
    """
    For now this is in python, which sucks.
    """
    def __init__(self):
        # for debug
        self.computed = 0

    def apply(self, inputs):
        def pil_histogram(image):
            self.computed += 1
            if self.computed % 100 == 0:
                print("Computed {}".format(self.computed))
            return np.asarray(Image.fromarray(image).histogram())

        return [tf.py_func(pil_histogram, [inputs[0]], [tf.int64])]

    def get_input_dtypes(self):
        return [np.dtype('uint8')]

    def get_output_dtypes(self):
        return [(False, np.dtype('int64'))]

    def reset(self):
        pass
