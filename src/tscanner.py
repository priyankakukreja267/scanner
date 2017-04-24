class TScanner:
    """
    TScanner main access point
    """

    def __init__(self):
        #kernel_registry.initialize_kernel_registry()
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
        pass

    def declare_output(self, column):
        """
        Declare the named column as an output column (i.e. it will be present in the final database).
        """
        pass

    def run(self):
        """
        Runs the computation
        :return: A database instance?
        """
        pass
