from fastapi import APIRouter, Depends, HTTPException
import mongo.functions.role_functions as role_functions
import mongo.models.role_model as role_model
from .api_auth import authorize_token, check_permission
from typing import Optional

router_role = APIRouter(
    prefix="/role",
    tags=["Role"],
    responses={404: {"description": "Not found"}},
)

@router_role.post("/")
async def insert_new_role(role: role_model.Role, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        role = role_model.Role(**role.dict())
        if role_functions.create_role(role):
            return {"status": "Role created"}
        else:
            raise HTTPException(status_code=400, detail="Role already exists")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router_role.get("/")
async def get_role(id_or_name: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_name:
            if role_functions.get_role(id_or_name):
                return role_functions.get_role(id_or_name).dict()
            else:
                raise HTTPException(status_code=404, detail="Role not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_role.put("/add/permission/")
async def add_role_permission(id_or_name: Optional[str] = None, permission: role_model.Role.UpdatePermission = None, authenticated: bool = Depends(check_permission)):
    permission = role_model.Role.UpdatePermission(**permission.dict())
    if authenticated["permission"] == True:
            if id_or_name:
                if role_functions.update_role_permission(id_or_name, permission):
                    return {"status": "Role updated"}
                else:
                    raise HTTPException(status_code=404, detail="Role not found or permission already exists")
            else:
                raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_role.put("/delete/permission/")
async def delete_role_permission(id_or_name: Optional[str] = None, permission: role_model.Role.UpdatePermission = None, authenticated: bool = Depends(check_permission)):
    permission = role_model.Role.UpdatePermission(**permission.dict())
    if authenticated["permission"] == True:
            if id_or_name:
                if role_functions.delete_role_permission(id_or_name, permission):
                    return {"status": "Role updated"}
                else:
                    raise HTTPException(status_code=404, detail="Role not found or permission already deleted")
            else:
                raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_role.delete("/")
async def delete_role(id_or_name: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_name:
            if role_functions.delete_role(id_or_name):
                return {"status": "Role deleted"}
            else:
                raise HTTPException(status_code=404, detail="Role not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
