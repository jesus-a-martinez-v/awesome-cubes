"""
Loads the configuration data present in the filesystem into memory.
"""

import json
from pymongo import MongoClient
import os


def _load_persistence_config():
    """
    Loads configuration data into memory'
    """
    # Load configuration data from file.
    parent_dir = os.path.dirname(os.path.abspath(__file__))
    with open('%s/persistence.json' % parent_dir) as f:
        configuration = json.load(f)

    c = MongoClient(configuration['host'], configuration['port'])  # Client.
    db = c[configuration['db']]  # Database
    col = db[configuration['collection']]  # Collection

    return c, db, col

# Exportable values.
client, database, collection = _load_persistence_config()
