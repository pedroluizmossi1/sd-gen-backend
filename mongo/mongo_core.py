from pymongo import MongoClient
import mongo.mongo_models as mongo_models
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config

mongo_host = get_config('MONGODB', 'mongodb_host')
mongo_port = get_config('MONGODB', 'mongodb_port')
mongo_db = get_config('MONGODB', 'mongodb_db')
mongo_user = get_config('MONGODB', 'mongodb_user')
mongo_password = get_config('MONGODB', 'mongodb_password')

client = MongoClient("mongodb://" + mongo_user + ":" + mongo_password + "@" + mongo_host + ":" + mongo_port + "/" + mongo_db)
db = client['main']

collection_users = db['users']
collection_collection = db['collections']
collection_images = db['images']


#USER
def create_user(user: mongo_models.User):
    user = user
    if get_user_by_login(user.login):
        return False
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
    
def update_user(login, user: mongo_models.User.UserUpdate):
    if get_user_by_login(login):
        collection_users.update_one({"login": login}, {"$set": user.dict()})
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
