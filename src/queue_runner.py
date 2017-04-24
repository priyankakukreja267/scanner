"""
Higher-level functions to access the database from a Tensorflow graph
"""

from . import database
import tensorflow as tf


def setup_queues(input_columns, output_columns):
    """
    Sets up an input and an output queue, as well as threads that feed data into the input and out of the
    output.
    :param input_columns: 
    :param output_columns: 
    :return: 
    """
