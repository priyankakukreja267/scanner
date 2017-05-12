import tensorflow as tf
import threading
import itertools
import profilehooks
import numpy as np
import datetime


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

    def __init__(self, db, input_columns, batch_size=50):
        """
        Generate a QueueManager object from a database and a
        :param db: A Database object
        :param input_columns: Name of input columns
        """
        self.db = db

        self.input_types = [db.get_column_dtype(name) for name in input_columns]
        self.input_columns = input_columns.copy()
        self.batch_size = batch_size

        self.output_columns = None
        # self.output_queue = None

    @staticmethod
    def _make_placeholder_name(item, f_name):
        return "input_dequeue_" + str(item) + "_" + f_name

    def dequeue_many(self):
        """
        :return: A tensor that will dequeue an element from the input queue when run 
        """
        items = []
        for item in range(self.batch_size):
            placeholders = []
            for f_name, f_type in zip(self.input_columns, self.input_types):
                placeholders.append(tf.placeholder(f_type, name=self._make_placeholder_name(item, f_name)))
            items.append(placeholders)

        return items

    def enqueue_many(self, to_queue, colspecs):
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

    #@profilehooks.profile
    def run_on_files(self, sess, tensor, input_reader, output_writer):
        """
        Run the tensor sequentially on every file in the input reader, writing to the output
        writer.
        """
        print("Started thread")
        computed = 0

        for changed_file, row in input_reader:
            if changed_file:
                output_writer.next_file()

            feed_dict = dict()
            for f_name, val in zip(self.input_columns, row):
                feed_dict["input_dequeue_" + f_name + ":0"] = val

            output_writer.write_row(sess.run(tensor, feed_dict=feed_dict))
            computed += 1
            if computed % 100 == 0:
                print("Processed {} frames".format(computed))

        input_reader.close()
        output_writer.close()

        print("Thread done.")

    @staticmethod
    def _grouper(iterable, n):
        args = [iter(iterable)] * n
        return zip(*args)

    @profilehooks.profile
    def run_tensor(self, tensor):
        """
        Run the tensor over some number of threads.
        """
        if self.output_columns is None:
            raise Exception(
                "You must call enqueue first. Also if you haven't done so yet you're doing something wrong.")

        input_reader = self.db.readers(self.input_columns)[0]
        output_writer = self.db.writers(self.output_columns)[0]

        packets = self._grouper(input_reader, self.batch_size)

        frames = 0
        start_time = datetime.datetime.now()
        for packet in packets:
            changes = []
            feed_dict = dict()
            for i_row, (changed_file, row) in enumerate(packet):
                if changed_file:
                    print("change on ", i_row)
                    changes.append(i_row)

                for c_name, c_value in zip(self.input_columns, row):
                    feed_dict[self._make_placeholder_name(i_row, c_name) + ":0"] = c_value

            with tf.Session() as sess:
                output_rows = list(zip(*sess.run(tensor, feed_dict=feed_dict)))
            print(len(output_rows))

            for i_row, row in enumerate(output_rows):
                if i_row in changes:
                    output_writer.next_file()
                output_writer.write_row(row)

            frames += self.batch_size
            time_delta = datetime.datetime.now() - start_time
            print("Packet done. Computed {} frames in {}, {} fps.".format(frames, time_delta, frames / time_delta.total_seconds()))
