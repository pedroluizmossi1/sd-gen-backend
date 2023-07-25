from fastapi import APIRouter, Depends, HTTPException
import mongo.models.user_model as user_model
import mongo.models.folder_model as folder_model
import mongo.functions.user_functions as user_functions
import mongo.functions.folder_functions as folder_functions
import mongo.functions.user_folder_functions as user_folder_functions
from .api_auth import authorize_token, check_permission, check_plan
from pydantic import validate_model, ValidationError
from typing import Optional
import json
import sys


router_user_folder = APIRouter(
    prefix="/user/folder",
    tags=["User Folder"],
    responses={404: {"description": "Not found"}},
)

@router_user_folder.post("/create/")
async def create_user_folder(
    folder: folder_model.Folder.Insert,
    authenticated: bool = Depends(check_permission),
):
    if authenticated:
        plan_resource = check_plan(["FOLDERS"], authenticated["plan"])
        print(plan_resource)
        if user_folder_functions.count_user_folders(authenticated["login"]) >= plan_resource["FOLDERS"]:
            raise HTTPException(status_code=403, detail="User has reached the maximum number of folders allowed by their plan.")
        try:
            folder = folder_model.Folder(**folder.dict())
            folder.owner = authenticated["id"]
            if user_folder_functions.create_user_folder(authenticated["login"], folder) == True:
                return {"status": "Folder created"}
            else:
                raise HTTPException(status_code=400, detail="Error creating folder")
        except Exception as e:
            raise HTTPException(status_code=400, detail="Folder already exists or invalid data")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user_folder.get("/get/")
async def get_user_folder(
    id_or_folder: str,
    authenticated: bool = Depends(check_permission),
):
    if authenticated:
        if id_or_folder:
            folder = user_folder_functions.get_user_folder(authenticated["id"], id_or_folder)
            if folder:
                return folder
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user_folder.get("/get/all/")
async def get_user_folders(
    authenticated: bool = Depends(check_permission),
):
    if authenticated:
        folders = user_folder_functions.get_user_folders(authenticated["id"])
        if folders:
            return folders
        else:
            raise HTTPException(status_code=400, detail="Folders not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user_folder.delete("/delete/")
async def delete_user_folder(
    id_or_folder: str,
    authenticated: bool = Depends(check_permission),
):
    if authenticated:
        if id_or_folder:
            if user_folder_functions.delete_user_folder(authenticated["id"], id_or_folder):
                return {"status": "Folder deleted"}
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")



