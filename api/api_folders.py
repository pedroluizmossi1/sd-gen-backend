from fastapi import APIRouter, Depends, HTTPException
import mongo.functions.folder_functions as folder_functions
import mongo.models.folder_model as folder_model
from .api_auth import authorize_token, check_permission
from pydantic import validate_model, ValidationError
from typing import Optional
from bson.objectid import ObjectId

router_collection = APIRouter(
    prefix="/folder",
    tags=["Folder"],
    responses={404: {"description": "Not found"}},
)

@router_collection.post("/")
async def insert_new_folder(collection: folder_model.Folder.Insert, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        collection = folder_model.Folder(**collection.dict())
        collection.owner = ObjectId(authenticated["id"])
        if folder_functions.create_folder(collection):
            return {"status": "Folder created"}
        else:
            raise HTTPException(status_code=400, detail="Folder already exists")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_collection.get("/")
async def get_folder(id: Optional[str] = None, name: Optional[str] = None, owner: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id:
            collection = folder_functions.get_folder_by_id(id)
            if collection:
                return collection
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        elif name and owner:
            collection = folder_functions.get_folder_by_name(name, owner)
            if collection:
                return collection
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        elif owner:
            collections = folder_functions.get_folders_by_owner(owner)
            if collections:
                return collections
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_collection.delete("/")
async def delete_folder(id: Optional[str] = None, name: Optional[str] = None, owner: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id:
            if folder_functions.delete_folder_by_id(id):
                return {"status": "Folder deleted"}
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        elif name and owner:
            if folder_functions.delete_folder_by_name(name, owner):
                return {"status": "Folder deleted"}
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

    