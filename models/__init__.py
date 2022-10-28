"""
    Initialize module
"""

import models.engine.file_storage as fstorage

storage = fstorage.FileStorage()
storage.reload()
