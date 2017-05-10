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
        def pil_histogram(image):
            self.computed += 1
            if self.computed % 100 == 0:
                print("Computed {}".format(self.computed))
            return np.asarray(Image.fromarray(image).histogram())

        return [tf.py_func(pil_histogram, [inputs[0]], [tf.int64])]


    def apply(self, inputs):
        def brighten(image):
            return tf.image.adjust_brightness(Image.fromarray(image), self.delta)
        
        return [tf.py_func(brighten, [inputs[0]], [tf.uint8])]

    def get_input_dtypes(self):
        return [np.dtype('uint8')]

    def get_output_dtypes(self):
        return [(False, np.dtype('uint8'))]

    def reset(self):
        pass

class Brightness:
    def get_input_dtypes(self):
        """
        :return: A list of dtypes 
        """
        return self.input_dtypes

    def get_output_dtypes(self):
        """
        :return: A list of dtypes
        """
        return self.output_dtypes

    def apply(self, input_image):

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """
        pass
