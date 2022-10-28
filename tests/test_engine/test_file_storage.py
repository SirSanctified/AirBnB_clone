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
import json
import inspect


class TestFileStorage(unittest.TestCase):
    """
        The test cases for the members of the FileStorage class
    """

    @classmethod
    def setUpClass(cls):
        """
        Set up class method for the doc tests
        """
        cls.setup = inspect.getmembers(FileStorage, inspect.isfunction)

    def test_module_docstring(self):
        """
        Tests if module docstring documentation exist
        """
        self.assertTrue(len(FileStorage.__doc__) >= 1)

    def test_class_docstring(self):
        """
        Tests if class docstring documentation exist
        """
        self.assertTrue(len(FileStorage.__doc__) >= 1)

    def test_func_docstrings(self):
        """
        Tests if methods docstring documntation exist
        """
        for func in self.setup:
            self.assertTrue(len(func[1].__doc__) >= 1)

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
        fname = self.file._FileStorage__file_path
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
        self.assertEqual(self.file._FileStorage__objects, self.file.all())

    def test_new_sets_an_object_in_objects(self):
        """
            Check if new() add an object in the __objects dictionary
        """
        self.file.new(self.base)
        clname = type(self.base).__name__
        id = self.base.id
        key = f'{clname}.{id}'
        self.assertTrue(key in self.file._FileStorage__objects)

    def test_objects_keys_are_in_the_form_classname_id(self):
        """
            Test if the dictionary keys in __objects are in the format
            <classname>.<id>
        """
        self.file.new(self.base)
        clname = type(self.base).__name__
        id = self.base.id
        key = f'{clname}.{id}'
        self.assertTrue(key in self.file._FileStorage__objects.keys())

    def test_save_serializes_objects_to_file_path(self):
        """
            Test if save() is actually writing the contents of the __objects
            dictionary to a file specified in __file_path
        """
        self.file.new(self.base)
        self.file.save()
        with open(self.file._FileStorage__file_path) as myFile:
            dump = myFile.read()
        self.assertNotEqual(len(dump), 0)

    def test_reload_when_file_path_does_not_exist(self):
        """
            Check if reloads() does nothing when __file_path does not exist
        """
        before = self.file._FileStorage__objects
        self.file.reload()
        self.assertEqual(before, self.file._FileStorage__objects)
