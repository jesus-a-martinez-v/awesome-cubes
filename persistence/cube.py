"""
This module provides a series of functions to access and manipulate the cube data persisted.
"""

from bson import ObjectId
from bson.errors import InvalidId
from config.config import collection
from data.cube import Cube


def store(c):
    """
    Stores a cube.
    :param c: Cube instance to be stored.
    :return: Identifier of the cube just stored.
    """
    assert isinstance(c, Cube), 'Input must a be Cube object'

    document = {
        'cube': c.cube,
        'dimension': c.dimension
    }

    result = collection.insert_one(document)
    return str(result.inserted_id)


def get(c_id):
    """
    Retrieve a particular cube.
    :param c_id: Identifier of the cube to be retrieved.
    :return: Cube if found or None otherwise.
    """
    try:
        cube_object_id = ObjectId(c_id)
        cube = collection.find_one({'_id': cube_object_id})

        if cube:
            return _stringify_id(cube)

        return None
    except (TypeError, InvalidId):
        raise TypeError('Invalid cube id.')


def get_all():
    """
    Gets all cubes in databae.
    :return: List of documents that represent cubes.
    """
    cubes = collection.find({})
    return [_stringify_id(cube) for cube in cubes]


def delete(c_id):
    """
    Deletes a particular cube
    :param c_id: Identifier of the cube to be deleted.
    :return: True if deleted. False otherwise.
    """
    try:
        cube_object_id = ObjectId(c_id)
        result = collection.delete_one({'_id': cube_object_id})

        return result.deleted_count == 1
    except (TypeError, InvalidId):
        raise TypeError('Invalid cube id.')


def delete_all():
    """
    Removes all cubes in database.
    :return Number of elements deleted.
    """
    result = collection.delete_many({})
    return result.deleted_count


def update(c_id, c):
    """
    Updates a cube.
    :param c_id: Identifier of the cube to be updated.
    :param c: Actual cube with the data to be set.
    :return: True if successfully updated cube; False otherwise.
    """
    assert isinstance(c_id, str), 'Cube identifier must be string instance.'
    assert isinstance(c, Cube), 'cube parameter must be of type Cube.'
    try:
        cube_object_id = ObjectId(c_id)

        query = {'_id': cube_object_id}
        updates = {'$set': {'dimension': c.dimension, 'cube': c.cube}}

        result = collection.update_one(query, updates)

        return result.modified_count == 1
    except (TypeError, InvalidId):
        raise TypeError('Invalid cube id.')


# ===============================
# Private helper functions.
# ===============================
def _stringify_id(cube_document):
    """
    Converts a cube id into a string and returns the same cube.
    :param cube_document: Cube document to be processed.
    :return: Cube document with its '_id' field converted into string.
    """
    cube_document['_id'] = str(cube_document['_id'])
    return cube_document
