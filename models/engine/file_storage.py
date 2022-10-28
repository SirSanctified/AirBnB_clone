#!/usr/bin/python3

"""
    Define a module that handles all the storage of objects for later use.
    This module deals with file storage system
"""

import json


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
        json_obj = ''
        try:
            with open(FileStorage.__file_path) as infile:
                json_obj = json.load(infile)
            for k, v in json_obj.items():
                FileStorage.__objects[k] = BaseModel(**v)
        except Exception:
            pass
