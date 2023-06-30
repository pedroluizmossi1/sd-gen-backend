from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import json
import mongo.functions.user_functions as user_functions
import mongo.models.user_model as user_model
from redis_core import insert_json, get_json, delete_json, get_all_string_values, delete_all_string_values

auth_scheme = HTTPBearer()

router_auth = APIRouter(
    prefix="/auth",
    tags=["auth"],
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
    if login:
        login = user_functions.get_user_by_login_ret_id(login)
        if user_functions.get_user_permission(login, path):
            return True
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")

@router_auth.post("/login")
async def login(user_login: user_model.User.Login):
    user_login.login = user_login.login.lower()
    if user_functions.login_user(user_login.login, user_login.password):
        try:
            token = insert_json(json.dumps({"login":user_login.login}), 36000) 
            return {"message": "Login success", "token": token}
        except:
            raise HTTPException(status_code=500, detail="Failed to create token") 
    else:
        raise HTTPException(status_code=401, detail="Login failed")

@router_auth.post("/logout")
async def logout(login: str = Depends(authorize_token)):
    try:
        delete_all_string_values(login)
        return {"message": "Logout success"}
    except:
        raise HTTPException(status_code=500, detail="Failed to logout")
    
@router_auth.get("/check")
async def check(token: str):
    if get_json(token):
        return True
    else:
        raise HTTPException(status_code=401, detail="Token invalid")
    

    


