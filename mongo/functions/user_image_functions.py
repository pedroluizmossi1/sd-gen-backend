from pymongo import MongoClient
import pymongo
import mongo.mongo_core as mongo_core
import mongo.functions.folder_functions as folder_functions
import api.api_auth as api_auth
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def create_image(image, folder, user):
    try:
        image = image
        image = mongo_core.collection_images.insert_one(image.dict())
        if image:
            if mongo_core.is_valid_objectid(folder):
                folder = mongo_core.collection_folders.update_one({"_id": ObjectId(folder), "owner": user},{"$addToSet": {"images": ObjectId(image.inserted_id)}})
                return True
            elif mongo_core.is_valid_objectid(folder) == False:
                folder = mongo_core.collection_folders.update_one({"name": folder, "owner": user},{"$addToSet": {"images": ObjectId(image.inserted_id)}})
                return True
            else:
                return False
        else:   
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

