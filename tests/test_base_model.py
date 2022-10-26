#!/usr/bin/python3

"""
    Test all the properties of BaseModel
"""

import unittest
from uuid import uuid4
from datetime import datetime
import models.base_model as base_model

class TestBase(unittest.TestCase):
    """
        The class that houses all tests of the BaseModel class
    """
    def setUp(self):
        """
            The function to initialise the base class for testing
        """
        self.uid = str(uuid4())
        self.creation = datetime.now()
        self.updation = datetime.now()

        self.base = base_model.BaseModel()
        self.copy = base_model.BaseModel(**self.base.to_dict())
        self.without_kwargs = base_model.BaseModel(
                self.uid, self.creation, self.updation
                )
        self.with_args_and_kwargs = base_model.BaseModel(
                self.uid, self.creation, self.updation, **self.base.to_dict()
                )
    
    def tearDown(self):
        """
            Do the clean up after every testcase
        """
        del self.base
        del self.copy
        del self.without_kwargs
        del self.with_kwargs


    def test_id_is_str(self):
        """
            Test if id is of type string
        """
        self.assertTrue(isinstance(self.base.id, str))

    def test_id_has_len_of_36(self):
        """
            The id derived from uuid4() must be of length 36
        """
        self.assertEqual(36, len(self.base.id))

    def test_created_at_is_datetime(self):
        """
            Test if created_at is of type datetime
        """
        self.assertTrue(isinstance(self.base.created_at, datetime))

    def test_created_at_equals_creation_time(self):
        """
            Test if created_at ressembles the time the object is created
        """
        self.assertGreaterEqual(datetime.now(), self.base.created_at)

    def test_updated_at_is_datetime(self):
        """
            Test if updated_at is instance of datetime
        """
        self.assertTrue(isinstance(self.base.updated_at, datetime))

    def test_updated_at_is_equal_created_at_at_creation_time(self):
        """
            Check if updated_at is equal created_at during the time of object
            creation
        """
        self.assertTrue(self.base.created_at == self.base.updated_at)

    def test_save_is_updating_updated_at(self):
        """
            Check if save function is updating the updated_at time by checking
            that the update time is equal now
        """
        self.base.save()
        self.assertGreaterEqual(datetime.now(), self.base.updated_at)

    def test_updated_at_is_not_equal_created_at_after_saving(self):
        """
            After calling the save method of the base object,
            created_at must not equal updated_at
        """
        self.base.save()
        self.assertFalse(self.base.created_at == self.base.updated_at)
    
    def test_str_returns_correct_representation_of_base(self):
        """
            Test if str() returns [<class name>] (<self.id>) <self.__dict__>
        """
        d = self.base.__dict__
        clname = self.base.__class__.__name__
        self.assertEqual(f'[{clname}] ({self.base.id}) {d}', str(self.base))

    def test_to_dict_returns_a_dictionary(self):
        """
            Check if to_dict() returns a dictionary instance
        """
        self.assertTrue(isinstance(self.base.to_dict(), dict))

    def test_to_dict_created_at_is_str(self):
        """
            Check if the created_at attribute of the dictionary returned
            by to_dict() is of type string
        """
        self.assertTrue(isinstance(self.base.to_dict()['created_at'], str))

    def test_to_dict_updated_at_is_str(self):
        """
            Check if the updated_at attribute of the dictionary returned
            by to_dict() is of type string
        """
        self.assertTrue(isinstance(self.base.to_dict()['updated_at'], str))

    def test_to_dict_contains_class_key(self):
        """
            Check if the returned dictionary has a __class__ key
        """
        self.assertTrue('__class__' in self.base.to_dict().keys())

    def test_to_dict_class_key_s_value_is_this_classname(self):
        """
            Check if the value associated with the __class__ key
            is the class name of the object
        """
        clname = self.base.__class__
        self.assertEqual(clname, self.base.to_dict()['__class__'])

    def test_to_dict_returns_dict_attribute_of_object(self):
        """
            Check if self__dict__ is contained in the dictionary returned
            by to_dict()
        """
        self.assertTrue(
                self.base.to_dict().contains(self.base.__dict__)
                )

    def test_to_dict_created_at_attribute_is_in_iso_format(self):
        """
            Check if the created_at attribute is in iso format
        """
        iso = self.base.created_at.isoformat()
        self.assertTrue(iso == self.base.to_dict()['created_at'])

    def test_to_dict_updated_at_attribute_is_in_iso_format(self):
        """
            Check if the updated attribute is in iso format
        """
        iso = self.base.updated_at.isoformat()
        self.assertTrue(iso == self.base.to_dict()['updated_at'])

    def test_created_at_retained_when_kwargs_not_empty(self):
        """
            Test to make sure that created_at return from dictionary
            is the same as the original one
        """
        self.assertEqual(self.copy.created_at, self.base.created_at)

    def test_updated_at_retained_when_kwargs_not_empty(self):
        """
            Test if updated_at did not change when object was serialised
        """
        self.assertEqual(self.copy.updated_at, self.base.updated_at)

    def test_id_retained_when_kwargs_not_empty(self):
        """
            Check if id was not changed during serialization
        """
        self.assertEqual(self.copy.id, self.base.id)

    def test_args_is_not_used_for_id_when_kwargs_is_empty(self):
        """
            Check if id specified in *args is not used when kwargs is empty
        """
        self.assertFalse(self.without_kwargs.id == self.uid)

    def test_args_is_not_used_for_created_at_when_kwargs_is_empty(self):
        """
            Check if created_at in args is not used when kwargs is empty
        """
        self.assertFalse(self.without_kwargs.created_at == self.creation)

    def test_args_not_used_for_updated_at_when_kwargs_empty(self):
        """
            Check if updated_at in args is not used when kwargs is empty
        """
        self.assertFalse(self.without_kwargs.updated_at == self.updation)

    def test_args_not_used_for_id_when_kwargs_not_empty(self):
        """
            check if id in args is not used when kwargs not empty
        """
        self.assertFalse(self.with_kwargs.id == self.uid)

    def test_args_not_used_for_created_at_when_kwargs_not_empty(self):
        """
            Check if created_at in args not used when kwargs not empty
        """
        self.assertFalse(self.with_kwargs.created_at == self.creation)

    def test_args_not_used_for_updated_at_when_kwargs_not_empty(self):
        """
            Check if updated_at in args not used when kwargs not empty
        """
        self.assertFalse(self.with_kwargs.updated_at == self.updation)


