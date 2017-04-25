"""
This is a useless file, please disregard it.
"""

import tensorflow as tf
import numpy as np
import threading
import math


sess = tf.Session()
q = tf.FIFOQueue(10, ['float', 'uint8'])
coord = tf.train.Coordinator()

arr_placeholder = tf.placeholder('float')
dig_placeholder = tf.placeholder('uint8')
enqueue_op = q.enqueue([arr_placeholder, dig_placeholder])

ex_count = 0


def load_examples(coord):
    if ex_count > 100:
        coord.request_stop()
    randarr = np.random.rand(10, 10)
    randdig = ex_count
    sess.run(enqueue_op, feed_dict={arr_placeholder: randarr, dig_placeholder: randdig})

ex = q.dequeue()
out = tf.reduce_mean(ex[0]) + ex[1]

def run_examples(coord):
    while not coord.should_stop():
        sess.run(out)

print(sess.run(out))
