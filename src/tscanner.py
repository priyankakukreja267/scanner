class TScanner:
    """
    TScanner main access point
    """

    def __init__(self):
        self.input = some input q.deque --> represents the tensor
        self.tensors['input'] = self.input
        self.stored_columns = list()
        self.db = Database("some_directory")

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
        self.tensors[inputcol] = qm.get_column_queue(input_columns)
        self.tensors[output_columns] = kernel.apply()
        # get next value in the same col from the Q manager
        # get the magic column over here, which will then be responsible for fetching the next one later on
        pass

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

        qm = QueueManager(db, self.tensors[input_columns])
        inputs = qm.dequeue()        
        # x = ... (depends on inputs, is a tuple of the correct stuff)
        out = qm.enqueue(x, (ColumnSpecification("out_col", video=True), ColumnSpecification("data_col", dtype='float')))        
        qm.run_tensor(out)


