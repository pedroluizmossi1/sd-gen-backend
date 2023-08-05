from pymongo import MongoClient
import pymongo
import mongo.models.user_model as user_model
import mongo.mongo_core as mongo_core
import mongo.models.folder_model as folder_model
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
    try:
        user = mongo_core.collection_users.insert_one(user.dict())
        folder = folder_model.Folder(name="root", owner=user.inserted_id, description="root folder", is_public=False, is_active=True)
        folder = mongo_core.collection_folders.insert_one(folder.dict())
        mongo_core.collection_users.update_one({"_id": user.inserted_id}, {"$addToSet": {"folders": folder.inserted_id}})
        if user.inserted_id and folder.inserted_id:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def login_user(login, password):
    try:
        user = mongo_core.collection_users.find_one({"login": login.lower()})
        mongo_core.collection_users.update_one({"login": login.lower()}, {"$currentDate": {"last_login": True}})
        if user:
            if password == password_decrypt(user["password"].decode()):
                return True
            else:
                return False
        else:
            return False    
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def logout_user(login):
    try:
        user = mongo_core.collection_users.find_one({"login": login.lower()})
        if user:
            mongo_core.collection_users.update_one({"login": login.lower()}, {"$currentDate": {"last_logout": True}})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def get_user_by_login(login):
    try:
        user = mongo_core.collection_users.find_one({"login": login})
        if user:
            return user
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def get_user_by_login_ret_id(login):
    try:
        user = mongo_core.collection_users.find_one({"login": login})
        if user:
            return user
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def get_user_by_id(id):
    try:
        user = mongo_core.collection_users.find_one({"_id": ObjectId(id)})
        if user:
            return user
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def get_user(id_or_login):
    if mongo_core.is_valid_objectid(id_or_login):
        return get_user_by_id(id_or_login)
    else:
        return get_user_by_login(id_or_login)

def get_all_users():
    try:
        users = mongo_core.collection_users.find()
        if users:

            return users
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def update_user_plan(login, plan):
    try:
        if get_user_by_login(login):
            user_plan_id = mongo_core.collection_plans.find_one({'name': plan})['_id']
            mongo_core.collection_users.update_one({"login": login}, {"$set": {"plan": user_plan_id}})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)
    
def update_user_role(login, role):
    try:
        if get_user_by_login(login):
            user_role_id = mongo_core.collection_roles.find_one({'name': role})['_id']
            mongo_core.collection_users.update_one({"login": login}, {"$set": {"role": user_role_id}})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def update_user(login, user):
    try:
        if get_user_by_login(login):
            try:
                user.password = password_encrypt(user.password)
            except AttributeError:
                mongo_core.collection_users.update_one({"login": login}, {"$set": user.dict(), "$currentDate": {"updated_at": True}})
                return True
        else:
            return False 
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def update_user_by_id(id, user):
    try:
        if get_user_by_id(id):
            try:
                user.password = password_encrypt(user.password)
            except AttributeError:
                mongo_core.collection_users.update_one({"_id": ObjectId(id)}, {"$set": user.dict()})
                return True
        else:
            return False 
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def update_user_password(login, password):
    try:
        user = get_user_by_login(login)
        if user:
            password = password_encrypt(password)
            mongo_core.collection_users.update_one({"login": login}, {"$set": {"password": password}, "$currentDate": {"updated_at": True, "last_password_change": True}})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)
        


    
def delete_user(login):
    try:
        user = mongo_core.collection_users.find_one({"login": login})
        if user:
            mongo_core.collection_users.delete_one({"login": login})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)
    
def delete_user_by_id(id):
    try:
        user = mongo_core.collection_users.find_one({"_id": ObjectId(id)})
        if user:
            mongo_core.collection_users.delete_one({"_id": ObjectId(id)})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)


# This code is used to get the permission of the user that is logged in. The permission is then used to check if the user is allowed to access the resource or not.

def get_user_permission(login, permission, method):
    try:
        user = mongo_core.collection_users.find_one({"_id": login})
        if user:
            user_role = mongo_core.collection_roles.find_one({"_id": ObjectId(user['role'])})
            if user_role:
                for role_permission_id in user_role['permissions']:
                    permission_list = mongo_core.collection_permissions.find_one({"_id": role_permission_id})
                    if permission_list:
                        if permission_list["resource"] == permission and permission_list["method"] == method:
                            return True
                return False
            return False
        return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def get_user_plan(login):
    try:
        user = mongo_core.collection_users.find_one({"login": login})
        if user:
            user_plan = mongo_core.collection_plans.find_one({"_id": ObjectId(user['plan'])})
            if user_plan:
                return user_plan
            else:
                return False
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)

def get_user_email(login):
    try:
        user = mongo_core.collection_users.find_one({"login": login})
        if user:
            return user['email']
        else:
            return False
    except pymongo.errors.PyMongoError as e:    
        mongo_core.handle_mongo_exceptions(e)