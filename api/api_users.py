from fastapi import APIRouter, Depends, HTTPException
from mongo.mongo_core import create_user, login_user, get_user_by_login, update_user
import mongo.mongo_models as mongo_models
from .api_auth import authorize_token 
import json
import sys


router_user = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router_user.post("/register")
async def register(user: mongo_models.User.UserInsert):
    user = mongo_models.User(**user.dict())
    user.login = user.login.lower()
    if create_user(user):
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=400, detail="User already exists")

@router_user.get("/profile/{login}")
async def profile(login: str, authenticated: bool = Depends(authorize_token)):
    print(authenticated)
    if authenticated == login:
        user = mongo_models.User(**get_user_by_login(login))
        #remove password from response
        user.password = ""
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user.post("/profile/{login}")
async def update_profile(login: str, user: mongo_models.User.UserUpdate, authenticated: bool = Depends(authorize_token)):
    if authenticated == login:
        user = mongo_models.User.UserUpdate(**user.dict())
        if update_user(login, user):
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    