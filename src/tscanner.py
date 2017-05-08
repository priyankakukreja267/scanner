import tensorflow as tf
import numpy as np
from src import database

class TScanner:
    """
    TScanner main access point
    """

    def __init__(self, some_dir):
        # self.input = some input q.deque --> represents the tensor
        nPixels = 400 * 600
        npArr = np.zeros(shape=(1,nPixels)) # SIZE??
        self.input = tf.Variable(npArr, name="input")
        self.stored_columns = list()
        self.db = database.Database(some_dir)

    def ingest(self, file_list):
        """
        Adds all the files to the database
        :param file_list: A list of files to add
        """
        self.db.ingest(file_list)

    def task(self, input_columns, kernel, output_columns):
        """
        Adds a task to the pipeline
        :param input_columns: (list of strings) The columns from which to get input from the kernel
        :param kernel: The kernel to run
        :param output_columns: (list of strings) The columns in which to write output from the kernel
        """
        # tensors is a dict for managing input and output data
        self.tensors['input_columns'] = input_columns # list of input cols
        self.qm = QueueManager(self.db, self.tensors['input_columns'])
        self.tensors['selected_columns'] = self.qm.get_selected_columns(input_columns) # ?
        self.tensors['output_columns'] = kernel.apply(input_columns) # list of output columns
        
    def declare_output(self, column):
        """
        Declare the named column as an output column (i.e. it will be present in the final database).
        add to a list of output columns
        """
        self.stored_columns.append(column)

    def run(self):
        """
        Runs the computation
        :return: A database instance?
        """
        #output = tf.tuple([self.tensors[col] for col in self.stored_columns])
        #output.run()

        inputs = self.qm.dequeue()
        out = self.qm.enqueue(inputs, (ColumnSpecification(self.tensors['output_columns'], video=True), ColumnSpecification(self.tensors['input_columns'], dtype='float')))
        qm.run_tensor(out)
