from pymongo import MongoClient
import pymongo
import mongo.models.image_model as image_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId


mongo_core.mongo_obj_str

def create_image(image: image_model.Image):
    try:
        image = image
        mongo_core.collection_images.insert_one(image.dict())
        return image
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)