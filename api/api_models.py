from fastapi import APIRouter, Depends, HTTPException
import mongo.functions.model_functions as model_functions
import mongo.models.model_model as model_model
from .api_auth import authorize_token, check_permission
from pydantic import validate_model, ValidationError
from typing import Optional
from bson.objectid import ObjectId

router_model = APIRouter(
    prefix="/model",
    tags=["Model"],
    responses={404: {"description": "Not found"}},
)

@router_model.post("/")
async def insert_new_model(model: model_model.Model, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        model = model_model.Model(**model.dict())
        if model_functions.create_model(model):
            return {"status": "Model created"}
        else:
            raise HTTPException(status_code=400, detail="Model already exists")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_model.get("/")
async def get_model(id_or_name: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated:
        if id_or_name:
            if model_functions.get_model(id_or_name):
                return model_functions.get_model(id_or_name)
            else:
                raise HTTPException(status_code=404, detail="Model not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_model.get("/all/")
async def get_all_models(authenticated: bool = Depends(check_permission)):
    if authenticated:
        return model_functions.get_models()
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router_model.delete("/")
async def delete_model(id_or_name: Optional[str] = None, authenticated: bool = Depends(check_permission)):
    if authenticated["permission"] == True:
        if id_or_name:
            if model_functions.delete_model(id_or_name):
                return {"status": "Model deleted"}
            else:
                raise HTTPException(status_code=404, detail="Model not found")
        else:
            raise HTTPException(status_code=400, detail="Missing parameter")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
