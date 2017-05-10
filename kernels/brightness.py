import tensorflow as tf
import numpy as np
from src.kernel import Kernel
from PIL import Image
import cv2

class Brightness(Kernel):
    """
    Takes an input_image and adjusts the brightness of the image by delta
    """
    def __init__(self, d=5):
        self.delta = d # default delta value
        print('brightness kernel inited')


    def apply(self, inputs):
        def brighten(image):
            return np.asarray(tf.image.adjust_brightness(input_image, self.delta))

        return [tf.py_func(brighten, [inputs[0]], [tf.uint8])]

    def get_input_dtypes(self):
        return [np.dtype('uint8')]

    def get_output_dtypes(self):
        return [(False, np.dtype('uint8'))]

    def reset(self):
        pass
