from pymongo import MongoClient
import pymongo
import mongo.models.user_model as user_model
import mongo.models.folder_model as folder_model
import mongo.mongo_core as mongo_core
import api.api_auth as api_auth
from .user_functions import get_user_by_login_ret_id
from .folder_functions import create_folder
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def count_user_folders(user):
    try:
        if mongo_core.is_valid_objectid(user):
            user = mongo_core.collection_users.find_one({"_id": ObjectId(user)})
            folders = user["folders"]
            return len(folders)
        elif mongo_core.is_valid_objectid(user) == False:
            user = mongo_core.collection_users.find_one({"login": user})
            folders = user["folders"]
            return len(folders)
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def create_user_folder(user, folder: folder_model.Folder):
    try:
        if mongo_core.is_valid_objectid(user):
            folder.owner = ObjectId(folder.owner)
            folder = mongo_core.collection_folders.insert_one(folder.dict())
            folder = mongo_core.collection_users.update_one({"_id": ObjectId(user)}, {"$addToSet": {"folders": ObjectId(folder.inserted_id)}})     
            return True
        elif mongo_core.is_valid_objectid(user) == False:
            folder.owner = ObjectId(folder.owner)
            folder = mongo_core.collection_folders.insert_one(folder.dict())
            folder = mongo_core.collection_users.update_one({"login": user}, {"$addToSet": {"folders": ObjectId(folder.inserted_id)}}) 
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def get_user_folder(owner, folder):
    try:
        owner = ObjectId(owner)
        if mongo_core.is_valid_objectid(folder):
            folder = mongo_core.collection_folders.find_one({"_id": ObjectId(folder)})
            try:
                if folder["owner"] == owner:
                    return folder
                else:
                    return False
            except:
                return False
        elif mongo_core.is_valid_objectid(folder) == False:
            folder = mongo_core.collection_folders.find_one({"owner": owner, "name": folder})
            if folder:
                return folder
            else:
                return False
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def get_user_folders(owner):
    try:
        owner = ObjectId(owner)
        user = mongo_core.collection_users.find_one({"_id": ObjectId(owner)})
        folders = user["folders"]
        folders_list = []
        for folder in folders:
            folder = mongo_core.collection_folders.find_one({"_id": ObjectId(folder)})
            folders_list.append(folder)
        return folders_list
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def delete_user_folder(owner, folder):
    try:
        folder = get_user_folder(owner, folder)
        if folder:
            for image in folder["images"]:
                mongo_core.collection_images.delete_one({"_id": ObjectId(image)})
            mongo_core.collection_folders.delete_one({"_id": ObjectId(folder["_id"])})
            user = mongo_core.collection_users.update_one({"_id": ObjectId(owner)}, {"$pull": {"folders": ObjectId(folder["_id"])}})
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

