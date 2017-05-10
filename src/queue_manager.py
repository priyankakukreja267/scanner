import tensorflow as tf
from multiprocessing import Pool
from multiprocessing.dummy import Pool as ThreadPool 
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
        self.input_reader = db.reader(self.input_columns)

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
        self.output_writer = self.db.writer(self.output_columns)

        return to_queue

    def run_tensor(self, tensor, nThreads=1):
        """
        :param tensor: The enqueue tensor to run
        """

        if self.output_columns is None:
            raise Exception(
                "You must call enqueue first. Also if you haven't done so yet you're doing something wrong.")

        with tf.Session() as sess:
            for changed_file, row in self.input_reader:
                if changed_file:
                    self.output_writer.next_file()

                feed_dict = dict()
                for f_name, val in zip(self.input_columns, row):
                    feed_dict["input_dequeue_" + f_name + ":0"] = val

                self.output_writer.write_row(sess.run(tensor, feed_dict=feed_dict))

    def do_work(self, sess, tensor, record):
        changed_file = record[0]
        row = record[1]
        if changed_file:
            self.output_writer.next_file()

        feed_dict = dict()
        for f_name, val in zip(self.input_columns, row):
            feed_dict["input_dequeue_" + f_name + ":0"] = val
        self.output_writer.write_row(sess.run(tensor, feed_dict=feed_dict))

    def t_run_tensor(self, tensor, nThreads=1):
        if self.output_columns is None:
            raise Exception(
                "You must call enqueue first. Also if you haven't done so yet you're doing something wrong.")

        with tf.Session() as sess:
            pool = ThreadPool(nThreads)
            pool.starmap(self.do_work, zip(itertools.repeat(sess), itertools.repeat(tensor), self.input_reader))
