from pymongo import MongoClient
import mongo.mongo_models as mongo_models
from crypto_dash.crypto_core import password_encrypt, password_decrypt

client = MongoClient("mongodb://python:python@localhost:27017/?authMechanism=DEFAULT&authSource=main")
db = client['main']

collection_users = db['users']
collection_collection = db['collections']
collection_images = db['images']


#USER
def create_user(user: mongo_models.User):
    user = user
    user.password = password_encrypt(user.password)
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
    
#COLLECTION

def create_collection(collection: mongo_models.Collection):
    collection = collection
    collection_collection.insert_one(collection.dict())
    return collection

def get_collection_by_name(name):
    collection = collection_collection.find_one({"name": name})
    if collection:
        return collection
    else:
        return False
    
def get_collection_by_owner(owner):
    collection = collection_collection.find_one({"owner": owner})
    if collection:
        return collection
    else:
        return False

#IMAGE

def create_image(image: mongo_models.Image):
    image = image
    collection_images.insert_one(image.dict())
    return image
