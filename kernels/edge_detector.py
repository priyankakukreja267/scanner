from src.kernel import Kernel
from PIL import Image
import tensorflow as tf
import numpy as np
import cv2

class Edge_Detector(Kernel):
    def __init__(self):
        print('edge_detector kernel inited')

    def get_input_dtypes(self):
        """
        :return: A list of dtypes 
        """
        return [np.dtype('uint8')]

    def get_output_dtypes(self):
        """
        :return: A list of dtypes
        """
        return [(True, np.dtype('uint8'))]

    def apply(self, input_columns):
        '''
        Takes an input_image and does custom operations
        '''
        def find_edges(image_data):
            #return cv2.Sobel(image_data, cv2.CV_64F, 1, 0, ksize=5)
            return np.uint8(np.absolute(cv2.Laplacian(image_data, cv2.CV_64F)))


        return [tf.py_func(find_edges, [input_columns[0]], tf.uint8)]

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """
        pass
