from fastapi import APIRouter, Depends, HTTPException
from mongo.mongo_core import create_folder, get_folder_by_name, get_folder_by_owner
import mongo.mongo_models as mongo_models


router_collection = APIRouter(
    prefix="/folder",
    tags=["folder"],
    responses={404: {"description": "Not found"}},
)

@router_collection.post("/")
async def insert(collection: mongo_models.Folder):
    return create_folder(collection)
    
    