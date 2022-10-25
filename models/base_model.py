#!/usr/bin/python3
"""
Define the BaseModel class

BaseModel defines all common attributes/methods for other classes

It will handle the initialization, serialization and
deserialization of all the instances

"""

import uuid
import datetime


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

    def __init__(self):
        """
        Initialize public instance attributes
        attributes:
            id (string): Unique id for each BaseModel
            created_at (datetime): Date and time of when an instance is created
            updated_at (datetime): Date and time of when an instance is updated
        """
        self.id = str(uuid.uuid4())
        self.created_at = datetime.datetime.today()
        self.updated_at = datetime.datetime.today()

    def __str__(self):
        """Returns string represantation in the format
        [<class name>] (<self.id>) <self.__dict__>"""
        return "[{}] ({}) {}".format(type(self).__name__, self.id, self.__dict__)

    def save(self):
        """Updates the public instance attribute updated_at
        with the current datetime"""
        self.updated_at = datetime.datetime.today()

    def to_dict(self):
        """Returns a dictionary containing all keys/values of the instance"""
        instance = vars(self)
        instance["created_at"] = self.created_at.isoformat()
        instance["updated_at"] = self.updated_at.isoformat()
        instance["__class__"] = type(self).__name__
        return instance
