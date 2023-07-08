from pymongo import MongoClient
import pymongo
import mongo.models.role_model as role_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def get_role(value):
    try:
        if mongo_core.is_valid_objectid(value):
            role = role_model.Role(**mongo_core.collection_roles.find_one({"_id": ObjectId(value)}))
            if role:
                return role
            else:
                return None
        else:
            role = role_model.Role(**mongo_core.collection_roles.find_one({"name": value}))
            if role:
                return role
            else:
                return None
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)
    
def create_role(role: role_model.Role):
    try:
        role = role
        mongo_core.collection_roles.insert_one(role.dict())
        return role
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def update_role_permission(value, permission):
    try:
        role = get_role(value)
        if role:
            update = mongo_core.collection_roles.update_one({"name": role.name}, {"$addToSet": {"permissions":{ "$each": permission.permissions}}})
            if update.modified_count >= 1:
                return True
            else:
                return False
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def delete_role_permission(value, permission):
    try:
        role = get_role(value)
        if role:
            update = mongo_core.collection_roles.update_one({"name": role.name}, {"$pull": {"permissions":
                                                                                            { "$in": permission.permissions}}})
            if update.modified_count >= 1:
                return True
            else:
                return False
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def delete_role(value):
    try:
        if mongo_core.is_valid_objectid(value):
            role = mongo_core.collection_roles.delete_one({"_id": ObjectId(value)})
        else:
            role = mongo_core.collection_roles.delete_one({"name": value})
        if role.deleted_count == 1:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def update_role_permission_md(name, permission):
    try:
        if get_role(name):
            role_permission_id = mongo_core.collection_permissions.find_one({'name': permission})['_id']
            mongo_core.collection_roles.update_one({"name": name}, {"$push": {"permissions": role_permission_id}})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)
