from pymongo import MongoClient
import pymongo
import mongo.mongo_models as mongo_models
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId
import re
import ast

mongo_host = get_config('MONGODB', 'mongodb_host')
mongo_port = get_config('MONGODB', 'mongodb_port')
mongo_db = get_config('MONGODB', 'mongodb_db')
mongo_user = get_config('MONGODB', 'mongodb_user')
mongo_password = get_config('MONGODB', 'mongodb_password')

client = MongoClient("mongodb://" + mongo_user + ":" + mongo_password + "@" + mongo_host + ":" + mongo_port + "/" + mongo_db)
db = client['main']

collection_users = db['users']
collection_folders = db['folders']
collection_images = db['images']
collection_roles = db['roles']
collection_plans = db['plans']
collection_permissions = db['permissions']
collection_list = {'users': mongo_models.User, 'folders': mongo_models.Folder, 'images': mongo_models.Image, 'roles': mongo_models.Role, 'plans': mongo_models.Plan, 
                   'permissions': mongo_models.Permission}


def check_collection(collection_name):
    collection = db[collection_name]
    if collection is not None:
        return True
    else:
        return False

def create_collection(collection_name):
    if check_collection(collection_name):
        collection = db[collection_name]
        collection.insert_one({})
        collection.delete_one({})
        print('Creating collection: ' + collection_name)
        return True
    else:
        return False

def delete_collection(collection_name):
    collection = db[collection_name]
    collection.drop()
    return True

def create_index(collection, index, type):
    collection = db[collection]
    if type == 'unique':
        collection.create_index(index, unique=True)
        print('Creating unique index: ' + index)
    elif type == 'index':
        collection.create_index(index),
        print('Creating index: ' + index)

         
def count_documents(collection):
    collection = db[collection]
    count = collection.count_documents({})
    return count        

def check_value(value):
    # Expressão regular para verificar se é uma string hexadecimal de 24 caracteres
    hex_pattern = re.compile(r"^[0-9a-fA-F]{24}$")

    if isinstance(value, bytes) and len(value) == 12:
        return value
    elif isinstance(value, str) and hex_pattern.match(value):
        return value
    else:
        return False

#GET BY ID
def get_document_by_id(collection, id):
    id = check_value(id)
    if id:
        document = collection.find_one({"_id": ObjectId(id)})
        if document:
            return document
        else:
            return False
    else:
        return False

#USER
def create_user(user: mongo_models.User):
    user = user
    if get_user_by_login(user.login):
        return False
    user.password = password_encrypt(user.password)
    user.plan = collection_plans.find_one({'name': 'free'})['_id']
    user.role = collection_roles.find_one({'name': 'user'})['_id']
    collection_users.insert_one(user.dict())
    return user

def login_user(login, password):
    user = collection_users.find_one({"login": login})
    if user:
        if password == password_decrypt(user["password"].decode()):
            return True
        else:
            return False
    else:
        return False
    
def get_user_by_login(login):
    user = collection_users.find_one({"login": login})
    if user:
        return user
    else:
        return False

def get_user_by_login_ret_id(login):
    user = collection_users.find_one({"login": login})['_id']
    if user:
        return user
    else:
        return False

def get_user_by_id(id):
    user = collection_users.find_one({"_id": ObjectId(id)})
    if user:
        return user
    else:
        return False

def update_user(login, user: mongo_models.User.UserUpdate):
    if get_user_by_login(login):
        collection_users.update_one({"login": login}, {"$set": user.dict()})
        return user
    else:
        return False

def update_user_plan(login, plan):
    if get_user_by_login(login):
        user_plan_id = collection_plans.find_one({'name': plan})['_id']
        collection_users.update_one({"login": login}, {"$set": {"plan": user_plan_id}})
        return True
    else:
        return False
    
def update_user_role(login, role):
    if get_user_by_login(login):
        user_role_id = collection_roles.find_one({'name': role})['_id']
        collection_users.update_one({"login": login}, {"$set": {"role": user_role_id}})
        return True
    else:
        return False
    
def get_user_permission(login, permission):
    user = collection_users.find_one({"login": 'admin'})
    if user:
        user_role = collection_roles.find_one({"_id": ObjectId(user['role'])})
        if user_role:
            for role_permission_id in user_role['permissions']:
                permission_list = collection_permissions.find_one({"name": permission})
                if permission_list["name"] == permission:
                    return True
            return False
        return False
    return False

#FOLDER

def create_folder(folder: mongo_models.Folder):
    folder = folder
    collection_folders.insert_one(folder.dict())
    return folder

def get_folder_by_name(name):
    folder = collection_folders.find_one({"name": name})
    if folder:
        return folder
    else:
        return False
    
def get_folder_by_owner(owner):
    folder = collection_folders.find_one({"owner": owner})
    if folder:
        return folder
    else:
        return False

#IMAGE

def create_image(image: mongo_models.Image):
    image = image
    collection_images.insert_one(image.dict())
    return image

# ROLE

def get_role_by_name(name):
    role = collection_roles.find_one({"name": name})
    if role:
        role = mongo_models.Role(**role)
        return role
    else:
        return None

def get_role_by_id(id):
    role = get_document_by_id(collection_roles, id)
    if role:
        role = mongo_models.Role(**role)
        return role
    else:
        return None
    
def create_role(role: mongo_models.Role):
    role = role
    collection_roles.insert_one(role.dict())
    return role

def update_role_permission(name, permission):
    if get_role_by_name(name):
        role_permission_id = collection_permissions.find_one({'name': permission})['_id']
        collection_roles.update_one({"name": name}, {"$push": {"permissions": role_permission_id}})
        return True
    else:
        return False

# PLAN

def get_plan_by_name(name):
    plan = collection_plans.find_one({"name": name})
    if plan:
        plan = mongo_models.Plan(**plan)
        return plan
    else:
        return None
    
def get_plan_by_id(id):
    plan = get_document_by_id(collection_plans, id)
    if plan:
        plan = mongo_models.Plan(**plan)
        return plan
    else:
        return None
    
def create_plan(plan: mongo_models.Plan):
    plan = plan
    collection_plans.insert_one(plan.dict())
    return plan

# PERMISSION

def get_permission_by_name(name):
    permission = collection_permissions.find_one({"name": name})
    if permission:
        permission = mongo_models.Permission(**permission)
        return permission
    else:
        return None
    
def get_permission_by_id(id):
    permission = get_document_by_id(collection_permissions, id)
    if permission:
        permission = mongo_models.Permission(**permission)
        return permission
    else:
        return None
    
