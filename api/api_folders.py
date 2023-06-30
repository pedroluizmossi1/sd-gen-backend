from fastapi import APIRouter, Depends, HTTPException
import mongo.functions.folder_functions as folder_functions
import mongo.models.folder_model as folder_model


router_collection = APIRouter(
    prefix="/folder",
    tags=["folder"],
    responses={404: {"description": "Not found"}},
)

@router_collection.post("/")
async def insert(collection: folder_model.Folder):
    return folder_functions.create_folder(collection)
    
    