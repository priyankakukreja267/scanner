import tensorflow as tf
import numpy as np

class Custom_kernel:

	def __init__(self):
		pass

	def get_input_dtypes(self):
		"""
		:return: A list of dtypes 
		"""
		input_dtypes = [np.dtype(np.uint8)]
		return input_dtypes

	def get_output_dtypes(self):
		"""
		:return: A list of dtypes
		"""
		output_dtypes = [np.dtype(np.uint8)]
		return output_dtypes

	def do_something(self, input_image):
		"""
		Houses the ops programmer might want
		"""
		pass

	def apply(self, input_image):
		'''
		Takes an input_image and does custom operations
		'''
		output_image = do_something(input_image)
		return output_image

	def reset(self):
		"""
		Forces the kernel to forget any internal state
		"""
		pass
