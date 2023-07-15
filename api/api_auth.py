from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
import mongo.functions.user_functions as user_functions
import mongo.functions.plan_functions as plan_functions
import mongo.models.user_model as user_model
import mongo.models.plan_model as plan_model
from redis_core import insert_json, get_json, delete_json, get_all_string_values, delete_all_string_values

auth_scheme = HTTPBearer()

router_auth = APIRouter(
    prefix="/auth",
    tags=["Auth"],
    responses={404: {"description": "Not found"}},
)

async def authorize_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    response = get_json(credentials.credentials)
    if response:
        return json.loads(response)["login"]
    else:
        raise HTTPException(status_code=401, detail="Token invalid")
    
async def check_permission(request: Request, login: str = Depends(authorize_token)):
    path = request.url.path
    method = request.method
    if login:
        login = user_functions.get_user_by_login_ret_id(login)
        login_id = login.get("_id")
        if user_functions.get_user_permission(login_id, path, method):
            return {"login": login.get("login"), "permission": True, "id": str(login_id), "plan": str(login.get("plan")), "token": request.headers.get("Authorization")}
        else:
            return {"login": login.get("login"), "permission": False, "id": str(login_id), "plan": str(login.get("plan")), "token": request.headers.get("Authorization")}
    else:
        return False
    
def check_plan(resources: list, plan: str):
    try:
        resources_dict = {}
        plan_dict = {}
        plan = plan_functions.get_plan(plan)
        for plan in plan["resources"]:
            plan_dict.update(plan)
            for resource in resources:
                resources_dict[resource] = plan_dict.get(resource)
        return resources_dict          
    except:
        return False

        

@router_auth.post("/login/")
async def user_login(user_login: user_model.User.Login):
    login = user_functions.login_user(user_login.login, user_login.password)
    token = insert_json(json.dumps({"login":user_login.login}), 36000)
    if login == True and token != False:
        return {"message": "Login success", "token": token}
    else:
        raise HTTPException(status_code=500, detail="Failed to login")
    


@router_auth.post("/logout/")
async def user_logout(login: str = Depends(authorize_token)):
    try:
        delete_all_string_values(login)
        return {"message": "Logout success"}
    except:
        raise HTTPException(status_code=500, detail="Failed to logout")
    
@router_auth.get("/check/")
async def check_token(token: str):
    if get_json(token):
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    

    


