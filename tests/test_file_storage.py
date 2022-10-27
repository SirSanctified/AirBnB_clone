#!/usr/bin/python3

"""
    Test the FileStorage class and its members
"""

import unittest
import os
import models.base_model as base_model
from models.engine.file_storage import FileStorage
from uuid import uuid4
from datetime import datetime


class TestFileStorage(unittest.TestCase):
    """
        The test cases for the members of the FileStorage class
    """

    def setUp(self):
        """
            Set up the objects to be used by all the tests
        """
        self.base = base_model.BaseModel()
        self.file = FileStorage()

    def tearDown(self):
        """
            Clean up everything after each testcase so that the test cases
            are independent of each other
        """
        fname = _FileStorage.__file_path
        del self.base
        del self.file
        if os.path.exists(fname):
            os.remove(fname)

    def test_all_returns_dictionary(self):
        """
            test if the all method returns a dictionary
        """
        self.assertTrue(isinstance(self.file.all(), dict))

    def test_all_returns_dictionary_objects(self):
        """
            Check if all() returns  dictionary __objects
        """
        self.assertEqual(_FileStorage.__objects, self.file.all())

    def test_new_sets_an_object_in_objects(self):
        """
            Check if new() add an object in the __objects dictionary
        """
        self.file.new(self.base)
        clname = type(self.base).__name__
        id = self.base.id
        key = f'{clname}.{id}'
        self.assertTrue(key in _FileStorage.__objects)

    def test_objects_keys_are_in_the_form_classname_id(self):
        """
            Test if the dictionary keys in __objects are in the format
            <classname>.<id>
        """
        self.file.new(self.base)
        clname = type(self.base).__name__
        id = self.base.id
        key = f'{clname}.{id}'
        self.assertEqual(key, _FileStorage.__objects.keys()[0])

    def test_save_serializes_objects_to_file_path(self):
        """
            Test if save() is actually writing the contents of the __objects
            dictionary to a file specified in __file_path
        """
        self.file.new(self.base)
        self.file.save()
        filename = _FileStorage.__file_path
        saved_json = ''
        with open(filename) as f:
            saved_json += f.read()
        self.assertEqual(json.dumps(_FileStorage.__objects, saved_json))

    def test_reloads_when_file_path_exists(self):
        """
            Check if reload() recreates the __objects from file
        """
        self.file.new(self.base)
        self.save()
        _FileStorage.__objects.clear()
        fname = _FileStorage.__file_path
        loaded_json = ''
        with open(fname) as f:
            loaded_json += f.read()

        self.file.reloads()
        self.assertEqual(_FileStorage.__objects, json.loads(loaded_json))

    def test_reload_when_file_path_does_not_exist(self):
        """
            Check if reloads() does nothing when __file_path does not exist
        """
        before = _FileStorage.__objects
        self.file.reloads()
        self.assertEqual(before, _FileStorage.__objects)
