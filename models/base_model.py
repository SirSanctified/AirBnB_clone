#!/usr/bin/python3

"""
    This module defines a base model that will be inherited by all the other
    classes.
    It handles the base functionality that all the other entities must possess
"""

from datetime import datetime
from uuid import uuid4
import json
from models import storage


class BaseModel:
    """
        attributes:
            id (string): Unique id for each BaseModel
            created_at (datetime): Date and time of when an instance is created
            updated_at (datetime): Date and time of when an instance is updated
        methods:
            __str__: Returns string represantation in the format
                     [<class name>] (<self.id>) <self.__dict__>
            save: Updates the public instance attribute updated_at with
                  the current datetime
            to_dict: Returns a dictionary containing all keys/values
                     of __dict__ of the instance
    """

    def __init__(self, *args, **kwargs):
        """
            Initialise ech model with a unique id,
            each having a creation timestamp as well as the updation timestamp
        """

        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = self.created_at
            storage.new(self)
        else:
            for k, v in kwargs.items():
                if k == "created_at":
                    self.created_at = datetime.fromisoformat(v)
                elif k == 'updated_at':
                    self.updated_at = datetime.fromisoformat(v)
                elif k == 'id':
                    self.id = v
                else:
                    continue

    def save(self):
        """
            Every time an object is saved, it's updated_at timestamp
            must be updated to the time the object was saved
        """
        self.updated_at = datetime.now()
        storage.save()

    def to_dict(self):
        """
            return the dictionary representation of this object
        """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = type(self).__name__
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        return dictionary

    def __str__(self):
        """
            Return the string representation of this object
            in the form [<class name>] (<self.id>) <self.__dict__>
        """
        clname = type(self).__name__
        return f'[{clname}] ({self.id}) {self.__dict__}'
