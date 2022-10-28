#!/usr/bin/python3

"""
    Define a city class
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
        Hold the attributes of a city
    """

    state_id = ''
    name = ''

    def __init__(self, *args, **kwargs):
        """init method for City class
        Attributes:
            args (list): The list with arguments
            kwargs (dict): A dictionary with arguments
        """
        super().__init__(*args, **kwargs)
