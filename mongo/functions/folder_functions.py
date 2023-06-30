from pymongo import MongoClient
import pymongo
import mongo.models.folder_model as folder_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def create_folder(folder: folder_model.Folder):
    folder = folder
    mongo_core.collection_folders.insert_one(folder.dict())
    return folder

def get_folder_by_name(name):
    folder = mongo_core.collection_folders.find_one({"name": name})
    if folder:
        return folder
    else:
        return False
    
def get_folder_by_owner(owner):
    folder = mongo_core.collection_folders.find_one({"owner": owner})
    if folder:
        return folder
    else:
        return False