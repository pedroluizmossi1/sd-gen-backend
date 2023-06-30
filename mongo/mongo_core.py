from pymongo import MongoClient
import pymongo
import mongo.models.role_model as role_model
import mongo.models.permission_model as permission_model
import mongo.models.plan_model as plan_model
import mongo.models.image_model as image_model
import mongo.models.user_model as user_model
import mongo.models.folder_model as folder_model
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId
import re
import ast
import pydantic


mongo_obj_str = pydantic.json.ENCODERS_BY_TYPE[ObjectId]=str
# This code is used to convert MongoDB's ObjectId to str
# It is used in MongoDB CRUD operations


mongo_host = get_config('MONGODB', 'mongodb_host')
mongo_port = get_config('MONGODB', 'mongodb_port')
mongo_db = get_config('MONGODB', 'mongodb_db')
mongo_user = get_config('MONGODB', 'mongodb_user')
mongo_password = get_config('MONGODB', 'mongodb_password')

client = MongoClient("mongodb://" + mongo_user + ":" + mongo_password + "@" + mongo_host + ":" + mongo_port)
db = client['main']

collection_users = db['users']
collection_folders = db['folders']
collection_images = db['images']
collection_roles = db['roles']
collection_plans = db['plans']
collection_permissions = db['permissions']
collection_list = {'users': user_model.User, 'folders': folder_model.Folder, 'images': image_model.Image, 'roles': role_model.Role, 'plans': plan_model.Plan, 
                   'permissions': permission_model.Permission}


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










    
