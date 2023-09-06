from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
import functions_core as functions_core
import mongo.functions.user_functions as user_functions
import mongo.functions.plan_functions as plan_functions
import mongo.models.user_model as user_model
import mongo.models.plan_model as plan_model
from redis_core import insert_json, get_json, delete_json, get_all_string_values, delete_all_string_values, insert_hash, get_hash, delete_hash
import random
import time

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
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
async def check_permission(request: Request, login: str = Depends(authorize_token)):
    """
    This function checks if the user with the given login has permission to access the requested resource.
    Parameters:
    - request: A FastAPI Request object representing the incoming HTTP request.
    - login: A string representing the user's login token. This parameter is optional and is obtained using the authorize_token dependency.
    Returns:
    - If the user has permission to access the requested resource, a dictionary containing the user's login, permission status, ID, plan, and token.
    - If the user does not have permission to access the requested resource, a dictionary containing the user's login, permission status, ID, plan, and token.
    - If the login parameter is not provided or is invalid, False.
    - If an error occurs, an HTTPException with a status code of 500 and a detailed error message.
    """
    path = request.url.path
    method = request.method
    try:
        if login:
            login = user_functions.get_user_by_login_ret_id(login)
            login_id = login.get("_id")
            if user_functions.get_user_permission(login_id, path, method):
                return {"login": login.get("login"), "permission": True, "id": str(login_id), "plan": str(login.get("plan")), "token": request.headers.get("Authorization")}
            else:
                return {"login": login.get("login"), "permission": False, "id": str(login_id), "plan": str(login.get("plan")), "token": request.headers.get("Authorization")}
        else:
            return False
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err
    
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

import asyncio 

@router_auth.post("/login/")
async def user_login(user_login: user_model.User.Login):
    """
    This function logs in a user with the given login and password.

    Parameters:
    - user_login: A Pydantic model representing the user's login credentials.

    Returns:
    - If the login is successful, a dictionary containing a success message and a token.
    - If the login fails, an HTTPException with a status code of 401 and a detailed error message.
    - If an error occurs, an HTTPException with a status code of 500 and a detailed error message.
    """
    login = user_functions.login_user(user_login.login, user_login.password)
    token = insert_json(json.dumps({"login":user_login.login}), 36000)
    if login is True and token is not False:
        return {"message": "Login success", "token": token, "ttl": 36000}
    else:
        raise HTTPException(status_code=401, detail="Failed to login, check your login or password")

    


@router_auth.post("/logout/")
async def user_logout(login: str = Depends(authorize_token)):
    """Logout user"""	
    try:
        user_functions.logout_user(login)
        delete_all_string_values(login)
        return {"message": "Logout success"}
    except:
        raise HTTPException(status_code=500, detail="Failed to logout")
    
@router_auth.get("/check/")
async def check_token(token: str):
    """Check token"""
    if get_json(token):
        return True
    else:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
@router_auth.post("/token/refresh/")
async def refresh_token(authenticated: bool = Depends(check_permission)):
    """Refresh token"""
    if authenticated:
        token = insert_json(json.dumps({"login":authenticated["login"]}), 36000)
        if token is not False:
            return {"message": "Token refreshed", "token": token, "ttl": 36000}
        else:
            raise HTTPException(status_code=500, detail="Failed to refresh token")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
@router_auth.post("/password/reset/token/",
                  summary="Send reset password token to email",
                  description="Send reset password token to email, TTL 5 minutes.")
async def reset_password_token(login: str):
    """Send reset password token to email"""
    try:
        ramdom_reset = random.randint(100000, 999999)
    except Exception as err:
        raise HTTPException(status_code=500, detail="Failed to generate reset code") from err
    json_data = {"login": login}
    user_email = user_functions.get_user_email(login)
    email = functions_core.send_email(user_email, "Reset password", "Your reset code is: " + str(ramdom_reset))
    if email is True:
        insert_hash(ramdom_reset, json_data, 300)
        return {"message": "Email sent"}
    else:
        raise HTTPException(status_code=500, detail=email)
        
@router_auth.put("/password/reset/",
                 summary="Reset password with token",
                 description="Reset password with token, TTL 5 minutes.")
async def reset_password(login: str, reset_token: int, new_password: str):
    """Reset password with token"""
    redis_data = get_hash(reset_token)
    decoded_data = {key.decode('utf-8'): value.decode('utf-8') for key, value in redis_data.items()}
    if decoded_data and decoded_data["login"] == login:
        user_functions.update_user_password(login, new_password)
        delete_hash(reset_token)
        return {"message": "Password reset success"}
    else:
        raise HTTPException(status_code=401, detail="Invalid reset token")
    
    

    


