import tensorflow as tf

class Custom_kernel:

	def do_something(input_image):
		pass

	def apply(input_image, delta):
		'''
		Takes an input_image and does custom operations
		'''
		output_image = do_something(input_image)
		return output_image

	def reset():
		pass
