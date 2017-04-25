"""
This is a useless file, please disregard it.
"""

import tensorflow as tf
import numpy as np


def do_stuff(input_tensor):
    return tf.reduce_mean(input_tensor[0]) + input_tensor[1] + input_tensor[1]

sess = tf.Session()

q = tf.FIFOQueue(10, ['float', 'float'])
enqueue_number = q.enqueue([tf.random_uniform((10, 10)), tf.random_uniform((1, ))])

x = q.dequeue()
out = do_stuff(x)

sess.run(enqueue_number)

print(sess.run(out))
