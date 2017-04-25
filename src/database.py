from .util.unique_id_dict import UniqueIDDict
from .column_specification import ColumnSpecification

import pickle
import cv2
import os


DEFAULT_COLUMN_NAME = "def_col"

class _ColumnReader:
    """
    Generator class that will output the rows of a table one by one. (Abstract)

    TODO: or should it be 100 lines per 100 lines, for instance?
    """
    def __next__(self):
        """Return the next row, as a NamedTuple"""
        raise NotImplementedError()

    def close(self):
        """Closes the file"""
        raise NotImplementedError()


class _DataColumnReader(_ColumnReader):
    def __init__(self, file_path):
        self.file = open(file_path)

    def __next__(self):
        return pickle.load(self.file)

    def __del__(self):
        self.close()

    def close(self):
        self.file.close()


class _VideoColumnReader(_ColumnReader):
    def __init__(self, file_path):
        self.file = cv2.VideoCapture(file_path, cv2.CAP_FFMPEG)
        if not self.file.isOpened():
            raise Exception("Could not open {}.".format(file_path))

    def __next__(self):
        ret, frame = self.file.read()
        if not ret:
            raise StopIteration
        return frame

    def __del__(self):
        self.close()

    def close(self):
        self.file.close()


class _ColumnWriter:
    def write_row(self, data):
        """Writes data in the next row in this column"""
        raise NotImplementedError()

    def close(self):
        """Closes the file"""
        raise NotImplementedError()


class _DataColumnWriter(_ColumnWriter):
    def __init__(self, file_path):
        self.file = open(file_path, 'w')

    def write_row(self, data):
        pickle.dump(data, self.file)

    def __del__(self):
        self.close()

    def close(self):
        self.file.close()


# TODO: VideoColumnWriter


class _Schema:
    def __init__(self, path):
        self.path = path
        try:
            with open(path) as schema_file:
                self.schema = pickle.load(schema_file)
        except FileNotFoundError:
            self.schema = {DEFAULT_COLUMN_NAME: ColumnSpecification(video=True)}

    def add_column(self, name, video, dtype):
        self.schema[name] = ColumnSpecification(video, dtype)

    def save(self):
        with open(self.path, 'w') as schema_file:
            pickle.dump(self, schema_file)


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

    def __init__(self, directory):
        """
        :param directory: The directory in which to store any additional database data
        """
        self.directory = directory
        self.files = UniqueIDDict()
        self.schema = _Schema(os.path.join(directory, ".schema"))

    def column_readers(self, column_name):
        """
        :return: a list of column readers for this column. There will be one per table in the database.
        """
        if column_name == DEFAULT_COLUMN_NAME:
            return [_VideoColumnReader(fname) for fname in self.files.objects()]

        if column_name not in self.schema.schema.keys():
            raise Exception("Unknown column {}".format(column_name))

        is_video = self.schema.schema[column_name]
        if is_video:
            return [_VideoColumnReader("{}_{}".format(id, column_name)) for id in self.files.ids()]
        else:
            return [_DataColumnReader("{}_{}".format(id, column_name)) for id in self.files.ids()]

    def add_column(self, name, video=False, dtype=None):
        """
        Adds a column to a database.
        :param name: Name of the new column
        :param video: Whether the column should be compressed as video data
        :return: A list of TableColumnGenerators.
        """
        if video:
            raise Exception("Writing new video columns is not yet supported.")

        if name == DEFAULT_COLUMN_NAME or name in self.schema.schema.keys():
            raise Exception("Column {} already exists.".format(name))

        self.schema.add_column(name, video, dtype)

        return [_DataColumnWriter("{}_{}".format(id, name)) for id in self.files.ids()]

    def ingest(self, files):
        """
        Adds files to the database.
        :param files: a list of file names
        """
        for file in files:
            self.files.add(file)

    def available_columns(self):
        """
        :return: A dictionnary of { column_name => is_video } representing all available columns
         in the database and whether they will be encoded as video.
        """
        return self.schema.schema.keys()

    def get_column_dtype(self, name):
        """
        :return: The dtype of the specified column
        """
        return self.schema.schema[name].dtype
