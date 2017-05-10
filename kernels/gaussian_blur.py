import tensorflow as tf
import numpy as np
import cv2

class Gaussian_Blur:
    def __init__(self, f=5):
        self.filter_size = f
        self.input_dtypes = [np.dtype(np.uint8)]
        self.output_dtypes = [np.dtype(np.uint8)]
        print('gaussian blurring kernel inited')

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

    def apply(self, input_columns):
        '''
        Takes an input_image and does custom operations
        '''
        input_image = input_columns[0]
        blur = cv2.GaussianBlur(img, (self.filter_size, self.filter_size), 0)
        return [blur]

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """

        pass
