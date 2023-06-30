from fastapi import APIRouter, Depends, HTTPException
from mongo.functions.role_functions import create_role, get_role_by_name, get_role_by_id
import mongo.models.role_model as role_model
from .api_auth import authorize_token, check_permission

router_role = APIRouter(
    prefix="/role",
    tags=["role"],
    responses={404: {"description": "Not found"}},
)

@router_role.post("/", dependencies=[Depends(check_permission)])
async def insert(role: role_model.Role):
    role = role_model.Role(**role.dict())
    if create_role(role):
        return {"status": "ok"}
    else:
        raise HTTPException(status_code=400, detail="Role already exists")

@router_role.get("/name/{name}", dependencies=[Depends(authorize_token)])
async def get_name(name: str):
    role = get_role_by_name(name)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")
    
@router_role.get("/id/{id}", dependencies=[Depends(authorize_token)])
async def get_id(id: str):
    role = get_role_by_id(id)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")
    
