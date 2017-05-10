from collections import OrderedDict


class UniqueIDDict:
    """
    A bidirectional dictionary between stuff and unique IDs
    """
    def __init__(self):
        self.obj_to_id = OrderedDict()
        self.id_to_obj = OrderedDict()
        self._id_counter = 0

    def add(self, obj, id=None):
        if id is None:
            id = self._id_counter
            self._id_counter += 1

        if id in self.id_to_obj:
            raise Exception("ID {} already taken.".format(id))

        self.obj_to_id[obj] = id
        self.id_to_obj[id] = obj

        return id

    def get_id(self, obj):
        return self.obj_to_id[obj]

    def get_obj(self, id):
        return self.id_to_obj[id]

    def objects(self):
        """Returns the object list. The objects are guaranteed to be in the same order as IDs in ids()"""
        return self.obj_to_id.keys()

    def ids(self):
        """Returns the IDs in order"""
        return self.obj_to_id.values()

    def reset(self):
        self.__init__()
