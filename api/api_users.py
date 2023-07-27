from fastapi import APIRouter, Depends, HTTPException
import mongo.models.user_model as user_model
import mongo.functions.user_functions as user_functions
from .api_auth import authorize_token, check_permission
from pydantic import validate_model, ValidationError
from typing import Optional
import json
import sys


router_user = APIRouter(
    prefix="/user",
    tags=["User"],
    responses={404: {"description": "Not found"}},
)

@router_user.post("/register/")
async def register_new_user(user: user_model.User.UserInsert):
    try:
        user = user_model.User(**user.dict())
        user.login = user.login.lower()
        user = user_functions.create_user(user)
        if user is True:
            return {"status": "User created"}
        elif user is False:
            raise HTTPException(status_code=400, detail="User already exists")
        else:
            raise HTTPException(status_code=400, detail="User not created")
    except ValidationError as e:
        raise HTTPException(status_code=500, detail=e.json())

@router_user.get("/profile/")
async def get_profile(login_or_id: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == False and login_or_id:
        if authenticated["login"] == user_functions.get_user(login_or_id)["login"]:
            user = user_model.User(**user_functions.get_user(login_or_id))
            user.password = ""
            return user
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    elif authenticated["permission"] == True and login_or_id:
        user = user_model.User(**user_functions.get_user(login_or_id))
        user.password = ""
        return user
    elif login_or_id is None:
        user = user_model.User(**user_functions.get_user(authenticated["login"]))
        user.password = ""
        return user
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
    
@router_user.delete("/profile/")
async def delete_user_profile(id: Optional[str] = None, login: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id:
            if user_functions.delete_user_by_id(id):
                return {"status": "User deleted"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        elif login:
            if user_functions.delete_user(login):
                return {"status": "User deleted"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
     
@router_user.put("/profile/first_last_name/")
async def update_user_profile_fl_name(id: Optional[str] = None, login: Optional[str] = None, user: user_model.User.UpdateFirstLastName = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == False:
        if id and authenticated["id"] == id:
            if user_functions.update_user_by_id(id, user):
                return {"status": "User updated"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        elif login and authenticated["login"] == login:
            if user_functions.update_user(login, user):
                return {"status": "User updated"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        elif login is None and id is None:
            if user_functions.update_user(authenticated["login"], user):
                return {"status": "User updated"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    elif authenticated["permission"] == True:
        if id:
            if user_functions.update_user_by_id(id, user):
                return {"status": "User updated"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        elif login:
            if user_functions.update_user(login, user):
                return {"status": "User updated"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        elif login is None and id is None:
            if user_functions.update_user(authenticated["login"], user):
                return {"status": "User updated"}
            else:
                raise HTTPException(status_code=400, detail="User not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")