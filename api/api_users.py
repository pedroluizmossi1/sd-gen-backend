from fastapi import APIRouter, Depends, HTTPException
import mongo.models.user_model as user_model
import mongo.functions.user_functions as user_functions
from .api_auth import authorize_token 
import json
import sys


router_user = APIRouter(
    prefix="/user",
    tags=["user"],
    responses={404: {"description": "Not found"}},
)

@router_user.post("/register")
async def register(user: user_model.User.UserInsert):
    user = user_model.User(**user.dict())
    user.login = user.login.lower()
    if user_functions.create_user(user):
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=400, detail="User already exists")

@router_user.get("/profile/{login}")
async def profile(login: str, authenticated: bool = Depends(authorize_token)):
    if authenticated == login:
        user = user_model.User(**user_functions.get_user_by_login(login))
        user.password = ""
        return user
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user.post("/profile/{login}")
async def update_profile(login: str, user: user_model.User.UserUpdate, authenticated: bool = Depends(authorize_token)):
    if authenticated == login:
        user = user_model.User.UserUpdate(**user.dict())
        if user_functions.update_user(login, user):
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=400, detail="User not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
    