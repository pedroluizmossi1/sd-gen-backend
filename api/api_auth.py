from fastapi import APIRouter, Depends, HTTPException
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
from mongo.mongo_core import login_user, get_user_permission, get_user_by_login_ret_id
import mongo.mongo_models as mongo_models
from redis_core import insert_json, get_json, delete_json

auth_scheme = HTTPBearer()

router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
)

@router_auth.post("/login")
async def login(user_login: mongo_models.User.Login):
    user_login.login = user_login.login.lower()
    if login_user(user_login.login, user_login.password):
        try:
            token = insert_json(json.dumps({"login":user_login.login}), 36000) 
            return {"message": "Login success", "token": token}
        except:
            raise HTTPException(status_code=500, detail="Failed to create token") 
    else:
        raise HTTPException(status_code=401, detail="Login failed")

@router_auth.post("/logout")
async def logout(user_logout: mongo_models.User.Logout):
    try:
        delete_json(user_logout.token)
        return {"message": "Logout success"}
    except:
        raise HTTPException(status_code=500, detail="Failed to Logout")
    
@router_auth.get("/check")
async def check(token: str):
    if get_json(token):
        return True
    else:
        raise HTTPException(status_code=401, detail="Token invalid")
    
async def authorize_token(credentials: HTTPAuthorizationCredentials = Depends(auth_scheme)):
    response = get_json(credentials.credentials)
    if response:
        return json.loads(response)["login"]
    else:
        raise HTTPException(status_code=401, detail="Token invalid")
    
async def check_permission(permission: str, login: str = Depends(authorize_token)):
    if login:
        login = get_user_by_login_ret_id(login)
        if get_user_permission(login, permission):
            return True
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    


