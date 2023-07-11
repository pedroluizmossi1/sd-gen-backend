from fastapi import APIRouter, Depends, HTTPException
import mongo.models.user_model as user_model
import mongo.models.folder_model as folder_model
import mongo.functions.user_functions as user_functions
import mongo.functions.folder_functions as folder_functions
import mongo.functions.user_folder_functions as user_folder_functions
from .api_auth import authorize_token, check_permission
from pydantic import validate_model, ValidationError
from typing import Optional
import json
import sys


router_user_folder = APIRouter(
    prefix="/user/folder",
    tags=["User Folder"],
    responses={404: {"description": "Not found"}},
)

@router_user_folder.post("/create")
async def create_user_folder(
    folder: folder_model.Folder.Insert,
    authenticated: bool = Depends(check_permission)
):
    if authenticated:
        try:
            folder = folder_model.Folder(**folder.dict())
            folder.owner = authenticated["id"]
            folder = user_folder_functions.create_user_folder(authenticated["login"], folder)
            return {"status": "Folder created"}
        except Exception as e:
            return e
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    



