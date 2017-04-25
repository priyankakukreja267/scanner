from . import database
import tensorflow as tf
import numpy as np


class QueueManager:
    """
    A higher-level manager to use the database.
    
    Normal usage::
    
        db = Database("some_directory")
        qm = QueueManager(db, input_columns)
        
        inputs = qm.dequeue()
        
        x = ... (depends on inputs, is a tuple of the correct stuff)
        
        out = qm.enqueue(x, (ColumnSpecification("out_col", video=True), ColumnSpecification("data_col", dtype='float')))
        
        qm.run_tensor(out)
        
    """
    def __init__(self, db, input_columns, output_columns):
        """
        Generate a QueueManager object from a database and a
        :param db: A Database object
        :param input_columns: Name of input columns
        :param output_columns: (name, colspec) tuples of output columns
        """
        input_fields = [(name, db.get_column_dtype(name)) for name in input_columns]
        self.input_queue = tf.FIFOQueue(100, np.dtype(input_fields))

        output_fields = [(name, dtype) for (name, dtype) in output_columns]
        self.output_queue = tf.FIFOQueue(100, np.dtype(output_fields))

    def dequeue(self):
        """
        :return: A tensor that will dequeue an element from the input queue when run 
        """
        return self.input_queue.dequeue()

    def enqueue(self, to_queue):
        """
        :return: A tensor that will enqueue the element when called
        """
        return self.output_queue.enqueue(to_queue)

    def run_tensor(self, ):
        """
        Starts two threads to fill up the input queue and empty the output queue.
        :return: A tf.Coordinator that signals when the processing pipeline should stop running.
        """
        pass
