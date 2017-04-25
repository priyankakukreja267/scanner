import tensorflow as tf
import numpy as np

class Brightness:

    def __init__(self):
    	self.delta = 5 # default delta value

    def get_input_dtypes(self):
        """
        :return: A list of dtypes 
        """
        input_dtypes = [np.dtype(np.uint8), np.dtype(np.uint8)]
        return input_dtypes

    def get_output_dtypes(self):
        """
        :return: A list of dtypes
        """
        output_dtypes = [np.dtype(np.uint8)]
        return output_dtypes

    def apply(self, input_image, delta):
		'''
		Takes an input_image and adjusts the brightness of the image by delta
		'''
		output_image = tf.image.adjust_brightness(input_image, delta)
		return output_image

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """
        pass
