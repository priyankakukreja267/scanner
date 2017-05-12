import tensorflow as tf
import numpy as np
import cv2
from src.kernel import Kernel


class DrawBoxKernel(Kernel):

    def get_input_dtypes(self):
        """
        :return: A list of dtypes 
        """
        return [np.dtype(np.uint8), np.dtype(np.int64)]

    def get_output_dtypes(self):
        """
        :return: A list of dtypes
        """
        return [(True, np.dtype(np.uint8))]

    def apply(self, input_columns):
        '''
        Takes an input_image and does custom operations
        '''
        def draw(img, coords):
            for i in range(0, len(coords), 4):
                x, y, w, h = coords[i:i+4]
                img = cv2.rectangle(img, (x,y), (x+w, y+h), (255, 0, 0), 2)

            return img

        return [tf.py_func(draw, [input_columns[0], input_columns[1][0]], tf.uint8)]

    def reset(self):
        """
        Forces the kernel to forget any internal state
        """

        pass
