# Write all the tensorflow code here to change brightness of a given image
import tensorflow as tf

class Brightness:

	def apply(input_image, delta):
		'''
		Takes an input_image and adjusts the brightness of the image by delta
		'''
		output_image = tf.image.adjust_brightness(input_image, delta)
		return output_image

	def reset():
		pass