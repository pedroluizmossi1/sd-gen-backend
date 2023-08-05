from pymongo import MongoClient
import pymongo
import mongo.models.user_model as user_model
import mongo.models.model_model as model_model
import mongo.mongo_core as mongo_core
import api.api_auth as api_auth
from .plan_functions import get_plan
from .model_functions import get_model
from bson.objectid import ObjectId

mongo_core.mongo_obj_str

def get_user_models_by_plan(owner):
    """Retrieves all models owned by a user."""
    try:
        owner = ObjectId(owner)
        user = mongo_core.collection_users.find_one({"_id": owner})
        plan = get_plan(str(user["plan"]))
        plan_models = {}

        if plan:
            for model_type, model_list in plan["resources"][0]["MODELS"].items():
                plan_models[model_type] = []
                for model in model_list:
                    plan_models[model_type].append(get_model(str(model)))
            return plan_models
        else:
            return {}                      
    except pymongo.errors.PyMongoError as err:
        mongo_core.handle_mongo_exceptions(err)
        return {}





