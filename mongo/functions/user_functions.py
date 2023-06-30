from pymongo import MongoClient
import pymongo
import mongo.models.user_model as user_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def create_user(user: user_model.User):
    user = user
    if get_user_by_login(user.login):
        return False
    user.password = password_encrypt(user.password)
    user.plan = mongo_core.collection_plans.find_one({'name': 'free'})['_id']
    user.role = mongo_core.collection_roles.find_one({'name': 'user'})['_id']
    mongo_core.collection_users.insert_one(user.dict())
    return user

def login_user(login, password):
    user = mongo_core.collection_users.find_one({"login": login})
    if user:
        if password == password_decrypt(user["password"].decode()):
            return True
        else:
            return False
    else:
        return False
    
def get_user_by_login(login):
    user = mongo_core.collection_users.find_one({"login": login})
    if user:
        user['role'] = str(user.get('role', ''))
        user['plan'] = str(user.get('plan', ''))
        return user
    else:
        return False

def get_user_by_login_ret_id(login):
    user = mongo_core.collection_users.find_one({"login": login})['_id']
    if user:
        return user
    else:
        return False

def get_user_by_id(id):
    user = mongo_core.collection_users.find_one({"_id": ObjectId(id)})
    if user:
        return user
    else:
        return False

def update_user(login, user: user_model.User.UserUpdate):
    if get_user_by_login(login):
        mongo_core.collection_users.update_one({"login": login}, {"$set": user.dict()})
        return user
    else:
        return False

def update_user_plan(login, plan):
    if get_user_by_login(login):
        user_plan_id = mongo_core.collection_plans.find_one({'name': plan})['_id']
        mongo_core.collection_users.update_one({"login": login}, {"$set": {"plan": user_plan_id}})
        return True
    else:
        return False
    
def update_user_role(login, role):
    if get_user_by_login(login):
        user_role_id = mongo_core.collection_roles.find_one({'name': role})['_id']
        mongo_core.collection_users.update_one({"login": login}, {"$set": {"role": user_role_id}})
        return True
    else:
        return False
    
# This code is used to get the permission of the user that is logged in. The permission is then used to check if the user is allowed to access the resource or not.

def get_user_permission(login, permission):
    user = mongo_core.collection_users.find_one({"_id": login})
    if user:
        user_role = mongo_core.collection_roles.find_one({"_id": ObjectId(user['role'])})
        if user_role:
            for role_permission_id in user_role['permissions']:
                permission_list = mongo_core.collection_permissions.find_one({"_id": role_permission_id})
                if permission_list:
                    if permission_list["resource"] == permission:
                        return True
            return False
        return False
    return False