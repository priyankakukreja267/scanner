class Database:
    """
    An image database. The database is stored on disk, and streamed as required.
    
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
        def __init__(self, vidfile, vid_id=None):
            pass

        def __del__(self):
            pass

        def __next__(self):
            """Return the next row"""
            pass

    def __init__(self, directory, videos=None):
        """
        :param directory: The directory in which to store any additional database data
        :param videos: An optional list of video files to create a database from
        """
        pass

    def get_table(self, name):
        """
        :return: a table generator for the named video
        """
        return self.TableGenerator(name)

    def table_generators(self):
        """
        :return: a list of all table generators in the database 
        """
        pass

    def add_column(self, name):
        pass
