class TScanner:
    """
    TScanner main access point
    """

    def __init__(self):
        self.input = some input q.deque --> represents the tensor
        self.tensors['input'] = self.input
        self.output_column_names = list()
        pass

    def ingest(self, file_list):
        """
        Adds all the files to the database
        :param file_list: A list of files to add
        """
        pass

    def task(self, input_columns, kernel, output_columns):
        """
        Adds a task to the pipeline
        :param input_columns: (list of strings) The columns from which to get input from the kernel
        :param kernel: The kernel to run
        :param output_columns: (list of strings) The columns in which to write output from the kernel
        """
        self.tensors[output_columns] = kernel(self.tensors[input_columns])
        pass

    def declare_output(self, column):
        """
        Declare the named column as an output column (i.e. it will be present in the final database).
        """
        add to a list of output columns
        pass

    def run(self):
        """
        Runs the computation
        :return: A database instance?
        """
        output = tf.tuple([self.tensors[col] for col in self.output_column_names])
        
        output.run()
        pass
