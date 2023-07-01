from fastapi import APIRouter, Depends, HTTPException
import mongo.models.user_model as user_model
import mongo.functions.user_functions as user_functions
from .api_auth import authorize_token, check_permission
from pydantic import validate_model, ValidationError
import json
import sys


router_user = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router_user.post("/register/")
async def register_new_user(user: user_model.User.UserInsert):
    user = user_model.User(**user.dict())
    user.login = user.login.lower()
    user = user_functions.create_user(user)
    if user is True:
        return {"status": "User created"}
    else:
        raise HTTPException(status_code=400, detail=user)

@router_user.get("/profile/by_login/")
async def get_profile_by_login(login: str, authenticated: bool = Depends(check_permission)):
    if authenticated["login"] == login and authenticated["permission"] == False:
        user = user_model.User(**user_functions.get_user_by_login(login))
        user.password = ""
        return user
    elif authenticated["permission"] == True:
        user = user_model.User(**user_functions.get_user_by_login(login))
        user.password = ""
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user.get("/profile/by_id/")
async def get_profile_by_id(id: str, authenticated: bool = Depends(check_permission)):
    if authenticated["login"] == id and authenticated["permission"] == False:
        user = user_model.User(**user_functions.get_user_by_id(id))
        user.password = ""
        return user
    elif authenticated["permission"] == True:
        user = user_model.User(**user_functions.get_user_by_id(id))
        user.password = ""
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user.put("/profile/by_token/")
async def update_user_profile_by_token(user: user_model.User.UpdateFirstLastName, authenticated: bool = Depends(check_permission)):
    if authenticated:
        if user_functions.update_user(authenticated["login"], user):
            return {"status": "Profile updated"}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router_user.get("/profile/all/")
async def get_all_users_profile(authenticated: bool = Depends(check_permission)):
    print(authenticated)
    user_list = []
    if authenticated["permission"] == True:
        users = user_functions.get_all_users()
        for user in users:
            user_list.append(user)
        return user_list            
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user.delete("/profile/by_id/")
async def delete_user_by_id(id: str, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if user_functions.delete_user_by_id(id):
            return {"status": "User deleted"}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user.delete("/profile/by_login/")
async def delete_user_by_login(login: str, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if user_functions.delete_user(login):
            return {"status": "User deleted"}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    