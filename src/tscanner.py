from src import database, queue_manager
import multiprocessing

class TScanner:
    """
    TScanner main access point
    """

    def __init__(self, db_directory='.db'):
        self.db = database.Database(db_directory)
        self.qm = None
        self.input_tensors = dict()
        self.input_columns = None
        self.column_tensors = dict()
        self.column_types = dict()
        self.output_columns = []

    def ingest(self, file_list):
        """
        Adds all the files to the database
        :param file_list: A list of files to add
        """
        self.db.ingest(file_list)

    def declare_inputs(self, columns):
        self.queue_manager = queue_manager.QueueManager(self.db, columns)
        input_tensors = list(zip(*self.queue_manager.dequeue_many()))
        print(input_tensors)
        for i_c, c in enumerate(columns):
            self.input_tensors[c] = input_tensors[i_c]

    def task(self, input_columns, kernel, output_columns):
        """
        Adds a task to the pipeline
        :param input_columns: (list of strings) The columns from which to get input from the kernel
        :param kernel: The kernel to run
        :param output_columns: (list of strings) The columns in which to write output from the kernel
        """
        if self.queue_manager is None:
            raise Exception("Call declare inputs first")

        # Check input columns
        kernel_input_tensors = []
        for ic in input_columns:
            if ic in self.input_tensors:
                kernel_input_tensors.append(self.input_tensors[ic])
            elif ic in self.column_tensors:
                kernel_input_tensors.append(self.column_tensors[ic])
            else:
                raise Exception("Unknown column {}".format(ic))

        # Check output columns
        for type, name in zip(kernel.get_output_dtypes(), output_columns):
            if name in self.column_tensors:
                raise Exception("Column {} already defined".format(name))
            self.column_types[name] = database.ColumnSpecification(name, video=type[0], dtype=type[1])

        # Send kernel output to correct column
        out = list(zip(*[kernel.apply(t) for t in zip(*kernel_input_tensors)]))
        
        for k_out, col_name in zip(out, output_columns):
            self.column_tensors[col_name] = k_out

    def declare_output(self, column):
        """
        Declare the named column as an output column (i.e. it will be present in the final database).
        """
        self.db.add_column(self.column_types[column])
        self.output_columns.append(column)

    def run(self):
        """
        Runs the computation
        :return: A database instance?
        """

        output = [self.column_tensors[c] for c in self.output_columns]
        colspecs = [self.column_types[c] for c in self.output_columns]
        enqueuer = self.queue_manager.enqueue_many(output, colspecs)
        self.queue_manager.run_tensor(enqueuer)

    def clear_db(self):
        self.db.clear()
