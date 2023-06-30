from pymongo import MongoClient
import pymongo
import mongo.models.role_model as role_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def get_role_by_name(name):
    role = role_model.Role(**mongo_core.collection_roles.find_one({"name": name}))
    if role:
        return role
    else:
        return None
    
def get_role_by_id(id):
    role = mongo_core.get_document_by_id(mongo_core.collection_roles, id)
    if role:
        role = role_model.Role(**role)
        return role
    else:
        return None
    
def create_role(role: role_model.Role):
    role = role
    mongo_core.collection_roles.insert_one(role.dict())
    return role

def update_role_permission(name, permission):
    if get_role_by_name(name):
        role_permission_id = mongo_core.collection_permissions.find_one({'name': permission})['_id']
        mongo_core.collection_roles.update_one({"name": name}, {"$push": {"permissions": role_permission_id}})
        return True
    else:
        return False