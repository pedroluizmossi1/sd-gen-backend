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
from fastapi import HTTPException
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
mongo_string = get_config('MONGODB', 'mongodb_string')
mongo_string_active = ast.literal_eval(get_config('MONGODB', 'mongodb_string_active'))

if mongo_string_active == False:
    client = MongoClient("mongodb://" + mongo_user + ":" + mongo_password + "@" + mongo_host + ":" + mongo_port + "/" + mongo_db)
else:
    client = MongoClient(mongo_string)
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
    try:
        if check_collection(collection_name):
            collection = db[collection_name]
            collection.insert_one({})
            collection.delete_one({})
            print('Creating collection: ' + collection_name)
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        handle_mongo_exceptions(e)

def delete_collection(collection_name):
    try:
        collection = db[collection_name]
        collection.drop()
        return True
    except pymongo.errors.PyMongoError as e:
        handle_mongo_exceptions(e)

def create_index(collection, index, type):
    try:
        collection = db[collection]
        if type == 'unique':
            collection.create_index(index, unique=True)
            print('Creating unique index: ' + index)
        elif type == 'index':
            collection.create_index(index),
            print('Creating index: ' + index)
        return True
    except pymongo.errors.PyMongoError as e:
        handle_mongo_exceptions(e)

         
def count_documents(collection):
    try:
        collection = db[collection]
        count = collection.count_documents({})
        return count     
    except pymongo.errors.PyMongoError as e:
        handle_mongo_exceptions(e)

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
    try:
        id = check_value(id)
        if id:
            document = collection.find_one({"_id": ObjectId(id)})
            if document:
                return document
            else:
                return False
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        handle_mongo_exceptions(e)
    
def get_document_by_field(collection, field, value):
    try:
        document = collection.find_one({field: value})
        if document:
            return document
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        handle_mongo_exceptions(e)
    
def is_valid_objectid(value):
    try:
        ObjectId(str(value))
        return True
    except:
        return False

def get_documents_id_or_field(collection, field, value):
    collection = db[collection]
    try:
        if is_valid_objectid(value):
            documents = get_document_by_id(collection, value)
        else:
            documents = get_document_by_field(collection, field, value)
        return documents
    except pymongo.errors.PyMongoError as e:
        handle_mongo_exceptions(e)

def handle_mongo_exceptions(exception):
    if isinstance(exception, pymongo.errors.AutoReconnect):
        raise HTTPException(status_code=500, detail="Database connection error.")
    elif isinstance(exception, pymongo.errors.BulkWriteError):
        raise HTTPException(status_code=500, detail="Error executing bulk operations.")
    elif isinstance(exception, pymongo.errors.CollectionInvalid):
        raise HTTPException(status_code=500, detail="The collection is invalid.")
    elif isinstance(exception, pymongo.errors.ConfigurationError):
        raise HTTPException(status_code=500, detail="Configuration error.")
    elif isinstance(exception, pymongo.errors.ConnectionFailure):
        raise HTTPException(status_code=500, detail="Database connection failure.")
    elif isinstance(exception, pymongo.errors.CursorNotFound):
        raise HTTPException(status_code=500, detail="Query cursor not found.")
    elif isinstance(exception, pymongo.errors.DocumentTooLarge):
        raise HTTPException(status_code=500, detail="The document is too large to be stored on the server.")
    elif isinstance(exception, pymongo.errors.DuplicateKeyError):
        key_value = exception.details.get('keyValue')
        raise HTTPException(status_code=500, detail="There is already a " + str(key_value) + " with this value.")
    elif isinstance(exception, pymongo.errors.EncryptionError):
        raise HTTPException(status_code=500, detail="Encryption or decryption error.")
    elif isinstance(exception, pymongo.errors.ExecutionTimeout):
        raise HTTPException(status_code=500, detail="Operation timeout reached.")
    elif isinstance(exception, pymongo.errors.InvalidName):
        raise HTTPException(status_code=500, detail="Invalid name used.")
    elif isinstance(exception, pymongo.errors.InvalidOperation):
        raise HTTPException(status_code=500, detail="Invalid operation.")
    elif isinstance(exception, pymongo.errors.InvalidURI):
        raise HTTPException(status_code=500, detail="Invalid MongoDB URI.")
    elif isinstance(exception, pymongo.errors.NetworkTimeout):
        raise HTTPException(status_code=500, detail="Network timeout exceeded.")
    elif isinstance(exception, pymongo.errors.NotPrimaryError):
        raise HTTPException(status_code=500, detail="The server is not the primary or is in recovery.")
    elif isinstance(exception, pymongo.errors.OperationFailure):
        raise HTTPException(status_code=500, detail=exception.details)
    elif isinstance(exception, pymongo.errors.ProtocolError):
        raise HTTPException(status_code=500, detail="Failure related to the communication protocol.")
    elif isinstance(exception, pymongo.errors.PyMongoError):
        raise HTTPException(status_code=500, detail="General PyMongo error.")
    elif isinstance(exception, pymongo.errors.ServerSelectionTimeoutError):
        raise HTTPException(status_code=500, detail="No MongoDB server available for the operation.")
    elif isinstance(exception, pymongo.errors.WTimeoutError):
        raise HTTPException(status_code=500, detail="Write operation timeout reached.")
    elif isinstance(exception, pymongo.errors.WaitQueueTimeoutError):
        raise HTTPException(status_code=500, detail="Timeout reached while waiting to checkout a connection from the pool.")
    elif isinstance(exception, pymongo.errors.WriteConcernError):
        raise HTTPException(status_code=500, detail="Write concern error.")
    elif isinstance(exception, pymongo.errors.WriteError):
        raise HTTPException(status_code=500, detail="Error during write operations.")
    else:
        raise HTTPException(status_code=500, detail="Unknown error.")




    
