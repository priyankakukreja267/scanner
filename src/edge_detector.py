import tensorflow as tf
import numpy as np
import cv2

class Edge_Detector:
    def __init__(self):
        self.input_dtypes = [np.dtype(np.uint8)]
        self.output_dtypes = [np.dtype(np.uint8)]
        print('edge_detector kernel inited')

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

    def do_something(self, input_image):
        """
        Houses the ops programmer might want
        """
        hor = cv2.Sobel(input_image, cv2.CV_64F, 1, 0, ksize=5)
        vert = cv2.Sobel(input_image, cv2.CV_64F, 0, 1, ksize=5)
        return hor, vert

    def apply(self, input_columns):
        '''
        Takes an input_image and does custom operations
        '''
        input_image = input_columns[0]
        hor, vert = do_something(input_image)
        return [hor, vert]

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """

        pass
