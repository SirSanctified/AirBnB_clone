#!/usr/bin/python3

"""
    This module defines a base model that will be inherited by all the other classes.
    It handles the base functionality that all the other entities must possess
"""

from datetime import datetime
from uuid import uuid4
import json


class BaseModel:
    """
        The base class with all base functionalities
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

    def to_dict(self):
        """
            return the dictionary representation of this object
        """
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__
        dictionary['created_at'] = dictionary['created_at'].isoformat()
        dictionary['updated_at'] = dictionary['updated_at'].isoformat()
        return dictionary

    def __str__(self):
        """
            Return the string representation of this object
            in the form [<class name>] (<self.id>) <self.__dict__>
        """
        clname = self.__class__.__name__
        return f'[{clname}] ({self.id}) {self.__dict__}'
