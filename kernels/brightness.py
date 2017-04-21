# Write all the tensorflow code here to change brightness of a given image

def adjust_brightness(input_image, delta):
	'''
	Takes an input_image and adjusts the brightness of the image by delta
	'''
	output_image = tf.image.adjust_brightness(image, delta)
	return output_image