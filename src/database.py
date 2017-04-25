from .util.unique_id_dict import UniqueIDDict
from .column_specification import ColumnSpecification
from collections import Iterator

import pickle
import cv2
import os


DEFAULT_COLUMN_NAME = "def_col"

class _ColumnReader(Iterator):
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

    @staticmethod
    def make_reader(video, files):
        if video:
            return _VideoColumnReader(files)
        else:
            return _DataColumnReader(files)


class _DataColumnReader(_ColumnReader):
    def __init__(self, files):
        self.files = files
        self.current_file = open(self.files[0], 'rb')

    def __next__(self):
        try:
            return pickle.load(self.current_file)
        except EOFError:
            self.current_file.close()
            del self.files[0]
            if not self.files:
                return StopIteration
            else:
                self.current_file = open(self.files[0], 'rb')
                return next(self)

    def __del__(self):
        self.close()

    def close(self):
        self.current_file.close()


class _VideoColumnReader(_ColumnReader):
    def _open_next_file(self):
        self.current_file = cv2.VideoCapture(self.files[0], cv2.CAP_FFMPEG)
        if not self.current_file.isOpened():
            raise Exception("Could not open {}.".format(self.files[0]))

    def __init__(self, files):
        self.files = files
        self._open_next_file()

    def __next__(self):
        ret, frame = self.current_file.read()
        if not ret:
            self.current_file.release()
            del self.files[0]
            if not self.files:
                raise StopIteration
            else:
                self._open_next_file()
                return next(self)
        return frame[:, :, ::-1]

    def __del__(self):
        self.close()

    def close(self):
        self.current_file.release()


class _ColumnWriter:
    def write_row(self, data):
        """Writes data in the next row in this column"""
        raise NotImplementedError()

    def next_file(self):
        """Returns the next file in sequence"""
        raise NotImplementedError()

    def close(self):
        """Closes the file"""
        raise NotImplementedError()

    @staticmethod
    def make_writer(video, files):
        if video:
            return _VideoColumnWriter(files)
        else:
            return _DataColumnWriter(files)


class _DataColumnWriter(_ColumnWriter):
    def __init__(self, files):
        self.files = files
        self.current_file = open(self.files[0], 'wb')

    def write_row(self, data):
        pickle.dump(data, self.current_file)

    def next_file(self):
        self.current_file.close()
        del self.files[0]
        self.current_file = open(self.files[0], 'wb')

    def __del__(self):
        self.close()

    def close(self):
        self.current_file.close()


class _VideoColumnWriter(_ColumnWriter):
    def _open_next_file(self):
        fourcc = cv2.VideoWriter_fourcc('H', '2', '6', '4')
        # TODO: have a way to set output parameters
        self.current_file = cv2.VideoWriter(self.files[0], fourcc, 20.0, (640, 480))

    def __init__(self, files):
        self.files = files
        self._open_next_file()

    def write_row(self, frame):
        self.current_file.write(frame[:, :, ::-1])

    def next_file(self):
        self.current_file.release()
        self._open_next_file()

    def close(self):
        self.current_file.release()


class _RowReader(Iterator):
    """
    A class to read rows of the specified columns
    """
    def __init__(self, column_readers):
        self.readers = column_readers

    def __next__(self):
        return [next(reader) for reader in self.readers]

    def close(self):
        for r in self.readers:
            r.close()


class _RowWriter(Iterator):
    """
    A class to write to rows, blah
    """
    def __init__(self, column_writers):
        self.writers = column_writers

    def write_row(self, data):
        for d, w in zip(data, self.writers):
            w.write_row(d)

    def next_file(self):
        for w in self.writers:
            w.next_file()

    def close(self):
        for w in self.writers:
            w.close()


class _Schema:
    def __init__(self, path):
        self.path = path
        self.columns = {DEFAULT_COLUMN_NAME: ColumnSpecification(DEFAULT_COLUMN_NAME, video=True)}
        self.save()

    def add_column(self, name, video, dtype):
        self.columns[name] = ColumnSpecification(name, video, dtype)
        self.save()

    def del_column(self, name):
        if name not in self.columns.keys():
            raise Exception("Unknown column {}")
        del self.columns[name]
        self.save()

    def save(self):
        with open(self.path, 'wb') as schema_file:
            pickle.dump(self, schema_file)

    @staticmethod
    def load_or_create(path):
        try:
            with open(path, 'rb') as schema_file:
                return pickle.load(schema_file)
        except FileNotFoundError:
            return _Schema(path)


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
        self.schema = _Schema.load_or_create(os.path.join(directory, ".schema"))

    def _fnames_for_col(self, column_name):
        if column_name == DEFAULT_COLUMN_NAME:
            return list(self.files.objects())

        if self.schema.columns[column_name].video:
            return ["{}_{}.mp4".format(fname, column_name) for fname in self.files.ids()]
        else:
            return ["{}_{}.dat".format(fname, column_name) for fname in self.files.ids()]

    def add_column(self, colspec):
        """
        Adds a column to a database.
        :param name: Name of the new column
        :param video: Whether the column should be compressed as video data
        """
        if colspec.name == DEFAULT_COLUMN_NAME or colspec.name in self.schema.columns.keys():
            raise Exception("Column {} already exists.".format(colspec.name))

        self.schema.add_column(colspec.name, colspec.video, colspec.dtype)

    def reader(self, column_names):
        """
        :return: a list of column readers for this column. There will be one per table in the database.
        """
        readers = []

        for column in column_names:
            if column not in self.schema.columns.keys():
                raise Exception("Unknown column {}".format(column))
            video = self.schema.columns[column].video
            readers.append(_ColumnReader.make_reader(video, self._fnames_for_col(column)))

        return _RowReader(readers)

    def writer(self, column_names):
        """
        :param column_names: Names of columns the reader should accept
        :return: 
        """
        writers = []

        for column in column_names:
            if column not in self.schema.columns.keys():
                raise Exception("Unknown column {}".format(column))
            video = self.schema.columns[column].video
            writers.append(_ColumnWriter.make_writer(video, self._fnames_for_col(column)))

        return _RowWriter(writers)

    def clear_column(self, column_name):
        self.schema.del_column(column_name)

        for file in self._fnames_for_col(column_name):
            print("** Removing {}".format(file))
            os.unlink(file)

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
        return self.schema.columns.keys()

    def get_column_dtype(self, name):
        """
        :return: The dtype of the specified column
        """
        return self.schema.columns[name].dtype
