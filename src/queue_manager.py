import tensorflow as tf
import threading
import itertools


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

        self.input_types = [db.get_column_dtype(name) for name in input_columns]
        self.input_columns = input_columns.copy()

        self.output_columns = None

        # self.input_queue = tf.FIFOQueue(100, self.input_fields)
        # self.output_queue = None

    def dequeue(self):
        """
        :return: A tensor that will dequeue an element from the input queue when run 
        """
        placeholders = []
        for f_name, f_type in zip(self.input_columns, self.input_types):
            placeholders.append(tf.placeholder(f_type, name="input_dequeue_" + f_name))
        return placeholders

    def enqueue(self, to_queue, colspecs):
        """
        :param to_queue: A list or tuple tensor with the types specified in colspecs
        :param colspecs: A list or tuple of column specifications
        :return: An enqueue tensor, which you want to pass to qm.run_tensor().
        """
        # if self.output_queue != None:
        #     raise Exception("You're trying to call enqueue more than once.")
        #
        # self.output_fields = [cs.get_dtype() for cs in colspecs]
        # self.output_queue = tf.FIFOQueue(100, self.output_fields)

        self.output_columns = [cs.name for cs in colspecs]

        return to_queue

    def run_on_files(self, sess, tensor, input_reader, output_writer):
        """
        Run the tensor sequentially on every file in the input reader, writing to the output
        writer.
        """
        print("Started thread")

        for changed_file, row in input_reader:
            if changed_file:
                output_writer.next_file()

            feed_dict = dict()
            for f_name, val in zip(self.input_columns, row):
                feed_dict["input_dequeue_" + f_name + ":0"] = val

            output_writer.write_row(sess.run(tensor, feed_dict=feed_dict))

    def run_tensor(self, tensor, n_threads=1):
        """
        Run the tensor over some number of threads.
        """
        if self.output_columns is None:
            raise Exception(
                "You must call enqueue first. Also if you haven't done so yet you're doing something wrong.")

        input_readers = self.db.readers(self.input_columns, n_threads)
        output_writers = self.db.writers(self.output_columns, n_threads)

        print(input_readers)
        print(output_writers)

        with tf.Session() as sess:
            thread_pool = [threading.Thread(target=self.run_on_files, args=(sess, tensor, ir, ow)) for (ir, ow) in
                           zip(input_readers, output_writers)]
            for thread in thread_pool:
                thread.start()
            for thread in thread_pool:
                thread.join()
