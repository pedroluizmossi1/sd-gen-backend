from pymongo import MongoClient
import pymongo
import mongo.models.plan_model as plan_model
import mongo.mongo_core as mongo_core
from crypto_dash.crypto_core import password_encrypt, password_decrypt
from config_core import get_config
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def get_plan_by_name(name):
    plan = mongo_core.collection_plans.find_one({"name": name})
    if plan:
        plan = plan_model.Plan(**plan)
        return plan
    else:
        return None
    
def get_plan_by_id(id):
    plan = mongo_core.get_document_by_id(mongo_core.collection_plans, id)
    if plan:
        plan = plan_model.Plan(**plan)
        return plan
    else:
        return None
    
def create_plan(plan: plan_model.Plan):
    plan = plan
    mongo_core.collection_plans.insert_one(plan.dict())
    return plan