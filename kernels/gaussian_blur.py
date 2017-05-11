import tensorflow as tf
import numpy as np
import cv2
from src.kernel import Kernel

class Gaussian_Blur(Kernel):
    def __init__(self, f=5):
        self.filter_size = f
        print('gaussian blurring kernel inited')

    def get_input_dtypes(self):
        """
        :return: A list of dtypes 
        """
        return [np.dtype(np.uint8)]

    def get_output_dtypes(self):
        """
        :return: A list of dtypes
        """
        return [(True, np.dtype(np.uint8))]

    def apply(self, input_columns):
        '''
        Takes an input_image and does custom operations
        '''
        def blur(img):
            return cv2.GaussianBlur(img, (self.filter_size, self.filter_size), 0)

        return [tf.py_func(blur, [input_columns[0]], tf.uint8)]

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """

        pass
