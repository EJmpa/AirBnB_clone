#!/usr/bin/python3

""" Module for serializing and deserializing instances to JSON and keeping
storage of instances
"""

import json
from models.base_model import BaseModel  # noqa
from models.user import User  # noqa
from models.state import State  # noqa
from models.city import City  # noqa
from models.place import Place  # noqa
from models.amenity import Amenity  # noqa
from models.review import Review  # noqa


class FileStorage:

    """ Class that stores and loads instances to/from files in JSON format """

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """ Returns the dictionary __objects """
        return FileStorage.__objects

    def new(self, obj):
        """ Sets in __objects the obj key <obj class name>.id """
        key_obj = "{}.{}".format(obj.__class__.__name__, obj.id)
        FileStorage.__objects[key_obj] = obj

    def save(self):
        """ serializes __objects to the JSON file (path: __file_path) """
        dict_obj = FileStorage.__objects
        dic_obj = {obj: dict_obj[obj].to_dict() for obj in dict_obj.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(dic_obj, f)

    def reload(self):
        """
        deserializes the JSON file to __objects (only if the JSON file
        (__file_path) exists ; otherwise, do nothing. If the file
        doesn’t exist, no exception should be raised)
        """
        try:
            with open(FileStorage.__file_path) as f:
                dic_obj = json.load(f)
                for obj_data in dic_obj.values():
                    class_name = obj_data["__class__"]
                    del obj_data["__class__"]
                    self.new(eval(class_name)(**obj_data))
        except FileNotFoundError:
            return
