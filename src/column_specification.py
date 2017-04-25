import numpy as np


class ColumnSpecification:
    def __init__(self, video=False, dtype=None):
        self.video = video
        if self.video:
            self.dtype = np.dtype('uint8')

        else:
            if dtype is None:
                raise Exception("For non-video columns, you must specify a dtype explicitly.")
            self.dtype = dtype
