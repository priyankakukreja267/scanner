class Database:
    """
    An image database. The database is stored on disk, and streamed as required.
    
             
    Usage:
         - To use a database as input, call table_generators(), which will return a list of TableGenerator objects,
           one per table in the database. A TableGenerator is a python generator and will sequentially return
           every row in the table
         - To add a column to the DB (as output), call add_column() with the name of the new column. This will
           return a list of TableColumnWriter objects (guaranteed to be in the same order as the TableGenerators
           returned by table_generators()), on which you can call write_row to write data into successive rows.
    
    Storage model:
         - Video files are stored on disk as video files
         - All other data is stored as a number of individual files, one per table, in serialized form.
    
    The original video file is left untouched, but all other potential files are stored in the database directory.
    The database_dir/.schema file stores the table schema in JSON format.
    """

    class TableGenerator:
        """
        Generator class that will output the rows of a table one by one.
        
        TODO: or should it be 100 lines per 100 lines, for instance?
        """
        def __init__(self, vidfile):
            pass

        def __del__(self):
            pass

        def __next__(self):
            """Return the next row, as a NamedTuple"""
            pass

    class TableColumnWriter:
        def __init__(self, table, column):
            pass

        def write_row(self, data):
            """Writes data in the next row in this column"""
            pass

    def __init__(self, directory):
        """
        :param directory: The directory in which to store any additional database data
        """
        self.files = []

    def table_generators(self):
        """
        :return: a list of all table generators in the database 
        """
        return [self.TableGenerator(fname) for fname in self.files]

    def add_column(self, name):
        """
        Adds a column to a database.
        :return: A list of TableColumnGenerators.
        """

    def ingest(self, files):
        self.files.extend(files.copy())
