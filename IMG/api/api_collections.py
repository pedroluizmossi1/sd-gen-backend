from fastapi import APIRouter, Depends, HTTPException
from mongo.mongo_core import create_collection, get_collection_by_name, get_collection_by_owner
import mongo.mongo_models as mongo_models


router_collection = APIRouter(
    prefix="/collection",
    tags=["collection"],
    responses={404: {"description": "Not found"}},
)

@router_collection.post("/")
async def insert(collection: mongo_models.Collection):
    return create_collection(collection)
    
    