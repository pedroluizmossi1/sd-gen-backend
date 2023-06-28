from .mongo_core import create_collection, collection_list, create_index, count_documents, db, create_user, update_user_role, update_user_plan, update_role_permission
import mongo.mongo_models as mongo_models
from importlib import import_module
import pandas as pd

def mongo_data_main():
    for collection in collection_list.keys():
        create_collection(collection)
        model_module = import_module('mongo.mongo_models')
        model_class = getattr(model_module, collection_list[collection].__name__)
        for index in model_class.Index.indexes:
            for type in index:
                create_index(collection, type[0], type[1])
    return True

admin_role = mongo_models.Role(name='admin', description='Administrator role', permissions=[])
admin_plan = mongo_models.Plan(name='admin', description='Administrator plan', price=0, resources={'admin': 'Administrator plan'})
user_role = mongo_models.Role(name='user', description='User role', permissions=[])
user_plan = mongo_models.Plan(name='free', description='User plan', price=0, resources={'user': 'User free plan'})

def mongo_start_data():
    collection_roles = db['roles']
    collection_plans = db['plans']
    if count_documents('permissions') == 0:
        collection_permissions = db['permissions']
        for index, row in permission_list.iterrows():
            collection_permissions.insert_one(row.to_dict())
    if count_documents('roles') == 0: 
        role_id = collection_roles.insert_one(admin_role.dict()).inserted_id
        role_id = collection_roles.insert_one(user_role.dict()).inserted_id
    if count_documents('plans') == 0:
        plan_id = collection_plans.insert_one(admin_plan.dict()).inserted_id
        plan_id = collection_plans.insert_one(user_plan.dict()).inserted_id
    if count_documents('users') == 0:
        admin = mongo_models.User(login='admin', password='admin', email='admin@admin.com', first_name='admin', last_name='admin', is_active=True)
        user = mongo_models.User(login='user', password='user', email='user@user.com', first_name='user', last_name='user', is_active=True)
        create_user(admin), create_user(user)
        update_user_role('admin', 'admin'), update_user_plan('admin', 'admin')
        update_user_role('user', 'user'), update_user_plan('user', 'free')

        for index, row in permission_list.iterrows():
            update_role_permission('admin', row['name'])

    return True


permission_list = pd.DataFrame(columns=['name', 'resource', 'description'])
permission_list = permission_list.append({'name': 'insert_role', 'resource': '/role/', 'description': 'Insert new role on database'}, ignore_index=True)
permission_list = permission_list.append({'name': 'get_role_by_name', 'resource': '/role/name/{name}', 'description': 'Get role by name'}, ignore_index=True)
permission_list = permission_list.append({'name': 'get_role_by_id', 'resource': '/role/id/{id}', 'description': 'Get role by id'}, ignore_index=True)