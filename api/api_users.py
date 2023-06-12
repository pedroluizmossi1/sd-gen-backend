from fastapi import APIRouter, Depends, HTTPException
from mongo.mongo_core import create_user, login_user, get_user_by_login
import mongo.mongo_models as mongo_models
from .api_auth import authorize_token 
import json
import sys


router_user = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router_user.post("/")
async def insert(user: mongo_models.User):
    return create_user(user)

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
    