# /usr/bin/python3
''' This module creates a variable that connects the objects
of the json with the programm. '''
from models.engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()
