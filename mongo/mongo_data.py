from .mongo_core import create_collection, collection_list, create_index, count_documents, db, collection_folders, client
import mongo.functions.role_functions as role_functions
import mongo.functions.plan_functions as plan_functions
import mongo.functions.permission_functions as permission_functions
import mongo.functions.user_functions as user_functions
import mongo.models.role_model as role_model
import mongo.models.permission_model as permission_model
import mongo.models.plan_model as plan_model
import mongo.models.image_model as image_model
import mongo.models.folder_model as folder_model
import mongo.models.user_model as user_model
from importlib import import_module
import pandas as pd

def mongo_data_main():
        client.drop_database('main')
        for collection in collection_list.keys():
            create_collection(collection)
            for index in collection_list[collection].Index.indexes:
                for type in index:
                    create_index(collection, type[0], type[1])

plan_resources = [{
                'SDXL_X': 1024,
                'SDXL_Y': 1024,
                'BASE_X': 1024,
                'BASE_Y': 1024,
                'HIGRESFIX': 2,
                'STEPS': 30,
                'SAMPLER': ["Euler", "Euler a", "UniPC"],
                'BATCH_SIZE': 2
                },
                {
                'FOLDERS': 10
                }]  
    

admin_role = role_model.Role(name='admin', description='Administrator role', permissions=[])
admin_plan = plan_model.Plan(name='admin', description='Administrator plan', price=0, resources= plan_resources)
user_role = role_model.Role(name='user', description='User role', permissions=[])
user_plan = plan_model.Plan(name='free', description='User plan', price=0, resources= plan_resources)

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
        admin = user_model.User(login='admin', password='admin', email='admin@admin.com', first_name='admin', last_name='admin', is_active=True, folders=[])
        user = user_model.User(login='user', password='user', email='user@user.com', first_name='user', last_name='user', is_active=True, folders=[])
        user_functions.create_user(admin), user_functions.create_user(user)
        user_functions.update_user_role('admin', 'admin'), user_functions.update_user_plan('admin', 'admin')
        user_functions.update_user_role('user', 'user'), user_functions.update_user_plan('user', 'free')

        for index, row in permission_list.iterrows():
            role_functions.update_role_permission_md('admin', row['name'])


    #Direct Index
    collection_folders.create_index([('owner', 1), ('name', 1)], unique=True)
    return True



permission_list = pd.DataFrame(columns=['name', 'resource', 'description'])
permission_list = permission_list.append({'name': 'get_profile', 'resource': '/user/profile/', 'method': "GET" , 'description': 'Get User profile by login'}, ignore_index=True)
permission_list = permission_list.append({'name': 'get_all_users_profile', 'resource': '/user/profile/all/', 'method': "GET" , 'description': 'Get all users profiles'}, ignore_index=True)
permission_list = permission_list.append({'name': 'update_user_profile_fl_name', 'resource': '/profile/first_last_name/', 'method': "PUT" , 'description': 'Update user profile'}, ignore_index=True)
permission_list = permission_list.append({'name': 'delete_user_profile', 'resource': '/user/profile/', 'method': "DELETE" , 'description': 'Delete user profile'}, ignore_index=True)
permission_list = permission_list.append({'name': 'get_role', 'resource': '/role/', 'method': "GET" , 'description': 'Get role'}, ignore_index=True)
permission_list = permission_list.append({'name': 'insert_new_role', 'resource': '/role/', 'method': "POST" , 'description': 'Insert new role'}, ignore_index=True)
permission_list = permission_list.append({'name': 'add_role_permission', 'resource': '/role/add/permission/', 'method': "PUT" , 'description': 'Update role'}, ignore_index=True)
permission_list = permission_list.append({'name': 'delete_role_permission', 'resource': '/role/delete/permission/', 'method': "PUT" , 'description': 'Delete role'}, ignore_index=True)
permission_list = permission_list.append({'name': 'delete_role', 'resource': '/role/', 'method': "DELETE" , 'description': 'Delete role'}, ignore_index=True)
permission_list = permission_list.append({'name': 'get_folder', 'resource': '/folder/', 'method': "GET" , 'description': 'Get folder'}, ignore_index=True)
permission_list = permission_list.append({'name': 'insert_new_folder', 'resource': '/folder/', 'method': "POST" , 'description': 'Insert new folder'}, ignore_index=True)
permission_list = permission_list.append({'name': 'delete_folder', 'resource': '/folder/', 'method': "DELETE" , 'description': 'Delete folder'}, ignore_index=True)
permission_list = permission_list.append({'name': 'insert_new_plan', 'resource': '/plan/', 'method': "POST" , 'description': 'Insert new plan'}, ignore_index=True)
permission_list = permission_list.append({'name': 'get_plan', 'resource': '/plan/', 'method': "GET" , 'description': 'Get plan'}, ignore_index=True)
permission_list = permission_list.append({'name': 'delete_plan', 'resource': '/plan/', 'method': "DELETE" , 'description': 'Delete plan'}, ignore_index=True)
permission_list = permission_list.append({'name': 'update_plan', 'resource': '/plan/', 'method': "PUT" , 'description': 'Update plan'}, ignore_index=True)
permission_list = permission_list.append({'name': 'get_all_plans', 'resource': '/plan/all/', 'method': "GET" , 'description': 'Get all plans'}, ignore_index=True)
permission_list = permission_list.append({'name': 'add_resource_to_plan', 'resource': '/plan/add/resource/', 'method': "PUT" , 'description': 'Add resource to plan'}, ignore_index=True)
permission_list = permission_list.append({'name': 'remove_resource_from_plan', 'resource': '/plan/update/resource/', 'method': "PUT" , 'description': 'Remove resource from plan'}, ignore_index=True)


plan_resources = [{
                'SDXL_X': '1024',
                'SDXL_Y': '1024',
                'BASE_X': '1024',
                'BASE_Y': '1024',
                'HIGRESFIX': '2'
                },
                {
                'FOLDERS': '10'
                }]