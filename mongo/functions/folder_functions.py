from pymongo import MongoClient
import pymongo
import mongo.models.folder_model as folder_model
from mongo.functions.user_functions import get_user_by_login_ret_id, get_user_by_id
import mongo.mongo_core as mongo_core
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def create_folder(folder: folder_model.Folder):
    try:
        folder = folder
        folder = mongo_core.collection_folders.insert_one(folder.dict())
        return folder
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)


def get_folder_by_name(name, owner):
    try:
        owner = get_user_by_id(owner)
        folder = mongo_core.collection_folders.find_one({"name": name, "owner": owner['_id']})
        if folder:
            return folder
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)
    
def get_folders_by_owner(owner, images=False):
    try:
        owner_id = get_user_by_login_ret_id(owner)
        folders = mongo_core.collection_folders.find({"owner": ObjectId(owner_id)})
        if folders:
            folders_header = []
            for folder in folders:
                folders_header.append({'id': str(folder['_id']),
                                        'owner': folder['owner'],
                                        'name': folder['name'], 
                                        'description': folder['description'], 
                                        'is_public': folder['is_public'],  
                                        'is_active': folder['is_active'], 
                                        'tags': folder['tags'],
                                        'images': folder['images'] if images else []
                                          })
            return folders_header
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def get_folder_by_id(id, images=False):
    try:
        folder = mongo_core.collection_folders.find_one({"_id": ObjectId(id)})
        if folder:
            folder_header = {'id': str(folder['_id']),
                                        'owner': folder['owner'],
                                        'name': folder['name'], 
                                        'description': folder['description'], 
                                        'is_public': folder['is_public'],  
                                        'is_active': folder['is_active'], 
                                        'tags': folder['tags'],
                                        'images': folder['images'] if images else []
                                          }
            return folder_header
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def delete_folder_by_id(id):
    try:
        folder = mongo_core.collection_folders.delete_one({"_id": ObjectId(id)})
        if folder:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def delete_folder_by_name(name, owner):
    try:
        owner = get_user_by_login_ret_id(owner)
        folder = mongo_core.collection_folders.delete_one({"name": name, "owner": owner})
        if folder:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def delete_all_folders_by_owner(owner):
    try:
        folder = mongo_core.collection_folders.delete_many({"owner": owner})
        if folder:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def update_folder_by_id(id, folder: folder_model.Folder.Update):
    try:
        folder = mongo_core.collection_folders.update_one({"_id": ObjectId(id)}, {"$set": folder.dict()})
        if folder:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def update_folder_by_name(name, folder: folder_model.Folder.Update):
    try:
        folder = mongo_core.collection_folders.update_one({"name": name}, {"$set": folder.dict()})
        if folder:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def update_folder_images_by_id(id, images):
    try:
        folder = mongo_core.collection_folders.update_one({"_id": ObjectId(id)}, {"$set": {"images": images}})
        if folder:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def update_folder_images_by_name(name, images):
    try:
        folder = mongo_core.collection_folders.update_one({"name": name}, {"$set": {"images": images}})
        if folder:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

