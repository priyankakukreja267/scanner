import tensorflow as tf
import numpy as np
import cv2

class Brightness:
    def __init__(self, d=5):
    	self.delta = d # default delta value
        self.input_dtypes = [np.dtype(np.uint8), np.dtype(np.uint8)]
        self.output_dtypes = [np.dtype(np.uint8)]
        print('brightness kernel inited')

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
		'''
		Takes an input_image and adjusts the brightness of the image by delta
		'''
		output_image = tf.image.adjust_brightness(input_image, self.delta)
		return [output_image]

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """
        pass
