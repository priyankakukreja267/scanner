# Write all the tensorflow code here to change brightness of a given image
import tensorflow as tf
import numpy as np
from src.kernel import Kernel


class BrightnessAdjustmentKernel(Kernel):
    def __init__(self, delta=5):
        self.delta = delta

    def apply(self, inputs):
        return [tf.image.adjust_brightness(inputs[0], self.delta)]

    def get_input_dtypes(self):
        return [np.dtype('uint8')]

    def get_output_dtypes(self):
        return [(True, np.dtype('uint8'))]

    def reset(self):
        pass
