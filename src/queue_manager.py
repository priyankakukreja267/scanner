from . import database
import tensorflow as tf
import numpy as np


class QueueManager:
    """
    A higher-level manager to use the database.
    
    Normal usage::
    
        db = Database("some_directory")
        qm = QueueManager(db, input_columns)
        
        inputs = qm.dequeue() # is a list of the input columns
        
        x = ... # (depends on inputs, is a list of the correct stuff)
        
        out = qm.enqueue(x, (ColumnSpecification("out_col", video=True), ColumnSpecification("data_col", dtype='float')))
        qm.run_tensor(out)
        
    """
    def __init__(self, db, input_columns):
        """
        Generate a QueueManager object from a database and a
        :param db: A Database object
        :param input_columns: Name of input columns
        """
        self.db = db

        input_fields = [db.get_column_dtype(name) for name in input_columns]
        self.input_queue = tf.FIFOQueue(100, input_fields)
        self.input_columns = input_columns

        self.output_queue = None

    def dequeue(self):
        """
        :return: A tensor that will dequeue an element from the input queue when run 
        """
        return self.input_queue.dequeue()

    def enqueue(self, to_queue, colspecs):
        """
        :param to_queue: A list or tuple tensor with the types specified in colspecs
        :param colspecs: A list or tuple of column specifications
        :return: An enqueue tensor, which you want to pass to qm.run_tensor().
        """
        if self.output_queue != None:
            raise Exception("You're trying to call enqueue more than once.")

        output_fields = [cs.get_dtype() for cs in colspecs]
        self.output_queue = tf.FIFOQueue(100, output_fields)

        return self.output_queue.enqueue(to_queue)

    def run_tensor(self, tensor):
        """
        :param tensor: The enqueue tensor to run
        """
        # OK we're doing bad stuff lol

        if self.output_queue is None:
            raise Exception(
                "You must call enqueue first. Also if you haven't done so yet you're doing something wrong.")

        input_generators = [self.db.column_readers(cname) for cname in self.input_columns]
        # Get generators for one file at a time
        input_generators = list(zip(*input_generators))

        for file in input_generators:
            for row in zip(*[file]):
                print()

        # DO STUFF HERE
