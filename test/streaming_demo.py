import tensorflow as tf
from PIL import ImageFilter, Image
import numpy as np
import cv2


video = cv2.VideoCapture("../data/kite.mkv", cv2.CAP_FFMPEG)
print(video.isOpened())

def blur(image):
    i = Image.fromarray(image)
    return np.asarray(i.filter(ImageFilter.BLUR), dtype=np.uint8)

with tf.Session():
    input = tf.placeholder(tf.uint8)
    blurred = tf.py_func(blur, [input], tf.uint8, stateful=False)
    res = blurred.eval(feed_dict={input: np.asarray(Image.open("/Users/matthieu/Pictures/photos correctes de moi/Yosemite1.png"), dtype=np.uint8)})

i = Image.fromarray(res).save("Image.png")
