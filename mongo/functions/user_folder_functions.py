from pymongo import MongoClient
import pymongo
import mongo.models.user_model as user_model
import mongo.models.folder_model as folder_model
import mongo.mongo_core as mongo_core
from .user_functions import get_user_by_login_ret_id
from .folder_functions import create_folder
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def create_user_folder(user, folder: folder_model.Folder):
    try:
        if mongo_core.is_valid_objectid(user):
            folder = folder = mongo_core.collection_folders.insert_one(folder.dict())
            folder = mongo_core.collection_users.update_one({"_id": ObjectId(user)}, {"$addToSet": {"folders": ObjectId(folder.inserted_id)}})     
            return True
        elif mongo_core.is_valid_objectid(user) == False:
            folder = mongo_core.collection_folders.insert_one(folder.dict())
            folder = mongo_core.collection_users.update_one({"login": user}, {"$addToSet": {"folders": ObjectId(folder.inserted_id)}}) 
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)