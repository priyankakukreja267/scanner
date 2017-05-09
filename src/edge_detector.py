from src.kernel import Kernel
from PIL import Image
import tensorflow as tf
import numpy as np
import cv2

class Edge_Detector(Kernel):
    def __init__(self):
        self.input_dtypes = [np.dtype('uint8')]
        self.output_dtypes = [(False, np.dtype('uint8')), (False, np.dtype('uint8'))] #[np.dtype('uint8')]
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

    def apply(self, input_columns):
        '''
        Takes an input_image and does custom operations
        '''
        # input_image = input_columns[0]
        
        # data = input_columns[0]
        # input_image = Image.fromarray(data, 'RGB') #np.asarray(Image.fromarray(input_columns[0]))
        def find_edges(image_data):
            img = np.asarray(Image.fromarray(image_data))
            edges = cv2.Sobel(input_image, cv2.CV_64F, 1, 0, ksize=5)
            return edges
        return [tf.py_func(find_edges, [input_columns[0]], [tf.uint8])]        

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """
        pass
