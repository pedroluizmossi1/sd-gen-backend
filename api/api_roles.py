from fastapi import APIRouter, Depends, HTTPException, Header
from mongo.mongo_core import create_role, get_role_by_name, get_role_by_id
import mongo.mongo_models as mongo_models
from .api_auth import authorize_token, check_permission
from typing import Optional

router_role = APIRouter(
    prefix="/role",
    tags=["role"],
    responses={404: {"description": "Not found"}},
)


def check_permission(permission: Optional[str] = Header('get_role_by_id', include_in_schema=False)):
    # Lógica de verificação do valor do parâmetro `permission`
    if permission:
        return permission
    else:
        raise HTTPException(status_code=400, detail="Role already exists")

@router_role.post("/")
async def insert(
    role: mongo_models.Role,
    permission: str = Depends(check_permission)
):
    if permission:
        role = mongo_models.Role(**role.dict())
        if create_role(role):
            return {"status": "ok"}
        else:
            raise HTTPException(status_code=400, detail="Role already exists")
    else:
        raise HTTPException(status_code=400, detail="Role already exists")

@router_role.get("/name/{name}")
async def get_name(name: str):
    role = get_role_by_name(name)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")
    
@router_role.get("/id/{id}")
async def get_id(id: str):
    role = get_role_by_id(id)
    if role:
        return role
    else:
        raise HTTPException(status_code=404, detail="Role not found")
    
