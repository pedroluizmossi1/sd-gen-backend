from pymongo import MongoClient
import pymongo
import mongo.models.permission_model as permission_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def get_permission_by_name(name):
    permission = mongo_core.collection_permissions.find_one({"name": name})
    if permission:
        permission = permission_model.Permission(**permission)
        return permission
    else:
        return None
    
def get_permission_by_id(id):
    permission = mongo_core.get_document_by_id(mongo_core.collection_permissions, id)
    if permission:
        permission = permission_model.Permission(**permission)
        return permission
    else:
        return None