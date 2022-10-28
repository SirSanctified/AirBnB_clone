#!/usr/bin/python3

"""
    Define a module that handles all the storage of objects for later use.
    This module deals with file storage system
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class FileStorage:
    """
        Serializes instances to a JSON file and deserializes
        JSON file to instances
    """

    __file_path = 'file.json'
    __objects = {}

    def all(self):
        """
            Return dictionary __objects containing all items
        """
        return FileStorage.__objects

    def new(self, obj):
        """
            Sets in __objects obj with key <obj classname>.id
        """
        key = f'{type(obj).__name__}.{obj.id}'
        FileStorage.__objects[key] = obj

    def save(self):
        """
            Serializes __objects to the JSON file in __file_path
        """
        dictionary = {}
        for k, v in FileStorage.__objects.items():
            dictionary[k] = v.to_dict()
        with open(FileStorage.__file_path, 'a') as outfile:
            json.dump(dictionary, outfile)

    def reload(self):
        """
            Deserializes the JSON file to __objects (only if the JSON file
            (__file_path) exists ; otherwise, do nothing.
            If the file doesn’t exist, no exception should be raised)
        """
        try:
            with open(FileStorage.__file_path, 'r') as my_file:
                for key, value in json.load(my_file).items():
                    if key not in FileStorage.__objects:
                        class_create = value['__class__']
                        if class_create == 'BaseModel':
                            FileStorage.__objects[key] = BaseModel(**value)
                        elif class_create == 'User':
                            FileStorage.__objects[key] = User(**value)
                        elif class_create == 'State':
                            FileStorage.__objects[key] = State(**value)
                        elif class_create == 'City':
                            FileStorage.__objects[key] = City(**value)
                        elif class_create == 'Amenity':
                            FileStorage.__objects[key] = Amenity(**value)
                        elif class_create == 'Place':
                            FileStorage.__objects[key] = Place(**value)
                        elif class_create == 'Review':
                            FileStorage.__objects[key] = Review(**value)
        except Exception:
            pass
