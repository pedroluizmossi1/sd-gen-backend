from pymongo import MongoClient
import pymongo
import mongo.models.model_model as model_model
import mongo.functions.plan_functions as plan_functions
import mongo.mongo_core as mongo_core
from bson.objectid import ObjectId
import pymongo.errors
import json

def create_model(model: model_model.Model):
    """
    Creates a new model in the database.

    Args:
        model: A `Model` object representing the model to create.

    Returns:
        The created `Model` object.

    Raises:
        pymongo.errors.PyMongoError: If there is an error communicating with the database.
    """
    try:
        model = mongo_core.collection_models.insert_one(model.dict())
        return model
    except pymongo.errors.PyMongoError as err:
        mongo_core.handle_mongo_exceptions(err)

def delete_model(value):
    """
    Deletes a model from the database.

    Args:
        value: The ID or name of the model to delete.

    Returns:
        True if the model was deleted, False otherwise.

    Raises:
        pymongo.errors.PyMongoError: If there is an error communicating with the database.
    """
    try:
        if mongo_core.check_value(value):
            mongo_core.collection_models.delete_one({"_id": ObjectId(value)})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as err:
        mongo_core.handle_mongo_exceptions(err)

def get_model(value):
    """
    Retrieves a model from the database.

    Args:
        value: The ID or name of the model to retrieve.

    Returns:
        A `Model` object representing the retrieved model, or None if the model was not found.

    Raises:
        pymongo.errors.PyMongoError: If there is an error communicating with the database.
    """
    try:
        if mongo_core.check_value(value):
            model = mongo_core.collection_models.find_one({"_id": ObjectId(value)})
            return model
        else:
            model = mongo_core.collection_models.find_one({"name": value})
            return model
    except pymongo.errors.PyMongoError as err:
        mongo_core.handle_mongo_exceptions(err)

def get_models():
    """
    Retrieves all models from the database.

    Returns:
        A list of dictionaries representing the retrieved models, or False if no models were found.

    Raises:
        pymongo.errors.PyMongoError: If there is an error communicating with the database.
    """
    try:
        models = mongo_core.collection_models.find()
        if models:
            models_header = []
            for model in models:
                models_header.append({'id': str(model['_id']),
                                        'name': model['name'], 
                                        'description': model['description'], 
                                        'is_public': model['is_public'],  
                                        'is_active': model['is_active'], 
                                        'tags': model['tags'],
                                        'image': model['image']
                                          })
            return models_header
        else:
            return False
    except pymongo.errors.PyMongoError as err:
        mongo_core.handle_mongo_exceptions(err)