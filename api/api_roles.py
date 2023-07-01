from fastapi import APIRouter, Depends, HTTPException
import mongo.functions.role_functions as role_functions
import mongo.models.role_model as role_model
from .api_auth import authorize_token, check_permission

router_role = APIRouter(
    prefix="/role",
    tags=["Role"],
    responses={404: {"description": "Not found"}},
)

@router_role.post("/", dependencies=[Depends(check_permission)])
async def insert_new_role(role: role_model.Role):
    role = role_model.Role(**role.dict())
    if role_functions.create_role(role):
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=400, detail="Role already exists")

@router_role.get("/name/", dependencies=[Depends(authorize_token)])
async def get_role_by_name(name: str):
    role = role_functions.get_role_by_name(name)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")
    
@router_role.get("/id/", dependencies=[Depends(authorize_token)])
async def get_role_by_id(id: str):
    role = role_functions.get_role_by_id(id)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")