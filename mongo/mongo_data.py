from .mongo_core import create_collection, collection_list, create_index, count_documents, db, collection_folders, client
import mongo.functions.role_functions as role_functions
import mongo.functions.plan_functions as plan_functions
import mongo.functions.permission_functions as permission_functions
import mongo.functions.user_functions as user_functions
import mongo.functions.model_functions as model_functions
import mongo.models.role_model as role_model
import mongo.models.permission_model as permission_model
import mongo.models.plan_model as plan_model
import mongo.models.image_model as image_model
import mongo.models.folder_model as folder_model
import mongo.models.user_model as user_model
import mongo.models.model_model as model_model
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
    'STEPS': 50,
    'SD15_SAMPLER': ["euler", "euler_ancestral", "uni_pc", "dpmpp_2m", "uni_pc_bh2"],
    'SDXL_SAMPLER': ["euler", "euler_ancestral", "uni_pc", "dpmpp_2m", "uni_pc_bh2"],
    'BATCH_SIZE': 2,
    'MODELS': {
        'SDXL': [],
        'REFINER': [],
        'SD15': [],
        'LATENT': []
    }
},
    {
    'FOLDERS': 10,
    'SDXL': True,
    'REFINER': True,
    'SD15': True,
    'LATENT': True
}]


admin_role = role_model.Role(
    name='admin', description='Administrator role', permissions=[])
admin_plan = plan_model.Plan(
    name='admin', description='Administrator plan', price=0, resources=plan_resources)
user_role = role_model.Role(
    name='user', description='User role', permissions=[])
user_plan = plan_model.Plan(
    name='free', description='User plan', price=0, resources=plan_resources)


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
        admin = user_model.User(login='admin', password='admin', email='admin@admin.com',
                                first_name='admin', last_name='admin', is_active=True, folders=[])
        user = user_model.User(login='user', password='user', email='user@user.com',
                               first_name='user', last_name='user', is_active=True, folders=[])
        user_functions.create_user(admin), user_functions.create_user(user)
        user_functions.update_user_role(
            'admin', 'admin'), user_functions.update_user_plan('admin', 'admin')
        user_functions.update_user_role(
            'user', 'user'), user_functions.update_user_plan('user', 'free')

        for index, row in permission_list.iterrows():
            role_functions.update_role_permission_md('admin', row['name'])
        for index, row in user_permissions.iterrows():
            role_functions.update_role_permission_md('user', row['name'])

    for index, row in model_list.iterrows():
        if row['version'] == 'SDXL':
            model_list_insert = model_model.Model(name=row['name'], description=row['description'],
                                                path=row['path'], is_public=row['is_public'], is_active=row['is_active'], type=row['type'], version=row['version'], info=SDXL_MODEL_INFO)
        elif row['version'] == 'SD15':
            model_list_insert = model_model.Model(name=row['name'], description=row['description'],
                                                path=row['path'], is_public=row['is_public'], is_active=row['is_active'], type=row['type'], version=row['version'], info=SD15_MODEL_INFO)
        else:
            model_list_insert = model_model.Model(name=row['name'], description=row['description'],
                                                path=row['path'], is_public=row['is_public'], is_active=row['is_active'], type=row['type'], version=row['version'], info={})
        model_inserted = model_functions.create_model(model_list_insert)
        plan_functions.add_model_to_plan(
            'admin', row['version'], model_inserted.inserted_id)
        plan_functions.add_model_to_plan(
            'free', row['version'], model_inserted.inserted_id)

    # Direct Index
    collection_folders.create_index([('owner', 1), ('name', 1)], unique=True)
    return True


SDXL_MODEL_INFO = {
    "width": 1024,
    "height": 1024,
    "steps": 15,
    "sampler_name": "dpmpp_2m",
    "cfg_scale": 7
}

SD15_MODEL_INFO = {
    "width": 512,
    "height": 768,
    "steps": 20,
    "sampler_name": "uni_pc",
    "cfg_scale": 7
}

model_list = pd.DataFrame(
    columns=['name', 'description', 'path', 'is_public', 'is_active', 'type', 'version', 'info'])
model_list = pd.concat([model_list, pd.DataFrame({'name': 'SDXL DreamShaper Alpha', 'description': 'SDXL Dream Shaper Alpha version',
                       'path': 'SDXL\\dreamshaperXL10_alpha2Xl10.safetensors', 'is_public': True, 'is_active': True, 'type': 'txt2img', 'version': 'SDXL',
                          'info': SDXL_MODEL_INFO}, index=[0])])
model_list = pd.concat([model_list, pd.DataFrame({'name': 'SD1.5 DreamShaper 8', 'description': 'SD1.5 Dream Shaper 8 version',
                       'path': 'Artistic\\dreamshaper_8.safetensors', 'is_public': True, 'is_active': True, 'type': 'txt2img', 'version': 'SD15',
                       'info': SD15_MODEL_INFO}, index=[0])])
model_list = pd.concat([model_list, pd.DataFrame({'name': 'SD1.5 Art Universe', 'description': 'This model was created by mixing several different models with each other, as well as adding about 10 LORA. This is an interesting model for creating images in the style of comics or cartoons.',
                                                  'path': 'Artistic\\artUniverse_v50.safetensors', 'is_public': True, 'is_active': True, 'type': 'txt2img', 'version': 'SD15',
                                                  'info': SD15_MODEL_INFO}, index=[0])])
model_list = pd.concat([model_list, pd.DataFrame({'name': 'SD1.5 Aniverse', 'description': 'SD1.5 Aniverse',
                                                  'path': 'Artistic\\aniverse_V12Pruned.safetensors', 'is_public': True, 'is_active': True, 'type': 'txt2img', 'version': 'SD15',
                                                  'info': SD15_MODEL_INFO}, index=[0])])
model_list = pd.concat([model_list, pd.DataFrame({'name': 'SD1.5 Reliberate', 'description': 'Reliberate model for those who need to work with photographic style. Yes, you can still create artwork, but it will look more like real artwork than digital.',
                                                  'path': 'Realistic\\reliberate_v20.safetensors', 'is_public': True, 'is_active': True, 'type': 'txt2img', 'version': 'SD15',
                                                  'info': SD15_MODEL_INFO}, index=[0])])

permission_list = pd.DataFrame(columns=['name', 'resource', 'description'])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'get_profile', 'resource': '/user/profile/',
                                           'method': "GET", 'description': 'Get User profile by login'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'get_all_users_profile', 'resource': '/user/profile/all/',
                                           'method': "GET", 'description': 'Get all users profiles'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'update_user_profile_fl_name', 'resource': '/profile/first_last_name/',
                                           'method': "PUT", 'description': 'Update user profile'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'delete_user_profile', 'resource': '/user/profile/',
                                           'method': "DELETE", 'description': 'Delete user profile'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'get_role', 'resource': '/role/',
                                           'method': "GET", 'description': 'Get role'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'insert_new_role', 'resource': '/role/',
                                           'method': "POST", 'description': 'Insert new role'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'add_role_permission', 'resource': '/role/add/permission/',
                                           'method': "PUT", 'description': 'Update role'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'delete_role_permission', 'resource': '/role/delete/permission/',
                                           'method': "PUT", 'description': 'Delete role'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'delete_role', 'resource': '/role/',
                                           'method': "DELETE", 'description': 'Delete role'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'get_folder', 'resource': '/folder/',
                                           'method': "GET", 'description': 'Get folder'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'insert_new_folder', 'resource': '/folder/',
                                           'method': "POST", 'description': 'Insert new folder'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'delete_folder', 'resource': '/folder/',
                                           'method': "DELETE", 'description': 'Delete folder'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'insert_new_plan', 'resource': '/plan/',
                                           'method': "POST", 'description': 'Insert new plan'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'get_plan', 'resource': '/plan/',
                                           'method': "GET", 'description': 'Get plan'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'delete_plan', 'resource': '/plan/',
                                           'method': "DELETE", 'description': 'Delete plan'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'update_plan', 'resource': '/plan/',
                                           'method': "PUT", 'description': 'Update plan'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'get_all_plans', 'resource': '/plan/all/',
                                           'method': "GET", 'description': 'Get all plans'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'add_resource_to_plan', 'resource': '/plan/add/resource/',
                                           'method': "PUT", 'description': 'Add resource to plan'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'remove_resource_from_plan', 'resource': '/plan/update/resource/',
                                           'method': "PUT", 'description': 'Remove resource from plan'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'get_user_image', 'resource': '/user/image/',
                                           'method': "GET", 'description': 'Get user image'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'delete_user_image', 'resource': '/user/image/',
                                           'method': "DELETE", 'description': 'Delete user image'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'generate_txt2img_v2_sdxl', 'resource': '/user/image/txt2img/v2/sdxl/',
                                           'method': "POST", 'description': 'Generate image from text'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'generate_txt2img_v2_sd15', 'resource': '/user/image/txt2img/v2/sd15/',
                                           'method': "POST", 'description': 'Generate image from text'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'add_model', 'resource': '/model/',
                                           'method': "POST", 'description': 'Add model'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                             pd.DataFrame({'name': 'delete_model', 'resource': '/model/',
                                           'method': "DELETE", 'description': 'Delete model'},
                                          index=[0])])
permission_list = pd.concat([permission_list,
                                pd.DataFrame({'name': 'upload_faceswap_image', 'resource': '/user/image/faceswap/upload/',
                                                'method': "POST", 'description': 'Upload faceswap image'},
                                                index=[0])]) 
permission_list = pd.concat([permission_list,
                                pd.DataFrame({'name': 'post_faceswap_image', 'resource': '/user/image/faceswap/',
                                                'method': "POST", 'description': 'Post faceswap image'},
                                                index=[0])])

user_permissions = pd.DataFrame(columns=['name', 'resource', 'description'])
user_permissions = pd.concat([user_permissions,
                              pd.DataFrame({'name': 'get_plan', 'resource': '/plan/',
                                            'method': "GET", 'description': 'Get plan'},
                                           index=[0])])
user_permissions = pd.concat([user_permissions,
                              pd.DataFrame({'name': 'get_user_image', 'resource': '/user/image/',
                                            'method': "GET", 'description': 'Get user image'},
                                           index=[0])])
user_permissions = pd.concat([user_permissions,
                              pd.DataFrame({'name': 'delete_user_image', 'resource': '/user/image/',
                                            'method': "DELETE", 'description': 'Delete user image'},
                                           index=[0])])
user_permissions = pd.concat([user_permissions,
                              pd.DataFrame({'name': 'generate_txt2img_v2_sdxl', 'resource': '/user/image/txt2img/v2/sdxl/',
                                            'method': "POST", 'description': 'Generate image from text'},
                                           index=[0])])
user_permissions = pd.concat([user_permissions,
                              pd.DataFrame({'name': 'generate_txt2img_v2_sd15', 'resource': '/user/image/txt2img/v2/sd15/',
                                            'method': "POST", 'description': 'Generate image from text'},
                                           index=[0])])
user_permissions = pd.concat([user_permissions,
                                pd.DataFrame({'name': 'upload_faceswap_image', 'resource': '/user/image/faceswap/upload/',
                                                'method': "POST", 'description': 'Upload faceswap image'},
                                                index=[0])])
user_permissions = pd.concat([user_permissions,
                                pd.DataFrame({'name': 'post_faceswap_image', 'resource': '/user/image/faceswap/',
                                                'method': "POST", 'description': 'Post faceswap image'},
                                                index=[0])])
