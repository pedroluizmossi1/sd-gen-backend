from pymongo import MongoClient
import pymongo
import mongo.models.plan_model as plan_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def get_plan(value):
    try:
        plan = mongo_core.get_documents_id_or_field("plans", "name", value)
        if plan:
            return plan
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def create_plan(plan: plan_model.Plan):
    try:
        plan = plan
        mongo_core.collection_plans.insert_one(plan.dict())
        return plan
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def update_plan(plan: plan_model.Plan, value):
    try:
        plan = plan
        plan = plan.dict()
        if mongo_core.is_valid_objectid(value):
            plan = mongo_core.collection_plans.update_one({"_id": ObjectId(value)}, {"$set": plan})
        else:
            plan = mongo_core.collection_plans.update_one({"name": value}, {"$set": plan})
        if plan.modified_count == 1:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)
        


def delete_plan(value):
    try:
        if mongo_core.is_valid_objectid(value):
            plan = mongo_core.collection_plans.delete_one({"_id": ObjectId(value)})
        else:
            plan = mongo_core.collection_plans.delete_one({"name": value})
        if plan.deleted_count == 1:
            return True
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)


def get_all_plans():
    try:
        plans = mongo_core.collection_plans.find()
        if plans:
            return plans
        else:
            return False
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def update_resource_from_plan(value, resource):
    try:
        if mongo_core.is_valid_objectid(value):
            plan = mongo_core.collection_plans.update_one({"_id": ObjectId(value)}, 
                                {"$set": {"resources": resource.resources}})
            return plan
        else:
            plan = mongo_core.collection_plans.update_one({"name": value}, 
                                {"$set": {"resources": resource.resources}})
            return plan
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)

def add_resource_to_plan(value, resource):
    try:
        if mongo_core.is_valid_objectid(value):
            plan = mongo_core.collection_plans.update_one(
                    {"_id": ObjectId(value)},
                    {"$addToSet": {"resources": {"$each": resource.resources}}}
                )
            return plan
        else:
            plan = mongo_core.collection_plans.find_one_and_update(
                    {"name": value},
                    {"$addToSet": {"resources": {"$each": resource.resources}}}
                )
            return plan
    except pymongo.errors.PyMongoError as e:
        mongo_core.handle_mongo_exceptions(e)
        