from fastapi import APIRouter, Depends, HTTPException
import mongo.models.user_model as user_model
import mongo.models.folder_model as folder_model
import mongo.functions.user_functions as user_functions
import mongo.functions.model_functions as model_functions
import mongo.functions.user_model_functions as user_model_functions
from .api_auth import authorize_token, check_permission, check_plan
from pydantic import validate_model, ValidationError
from typing import Optional
import json
import sys


router_user_model = APIRouter(
    prefix="/user/model",
    tags=["User Model"],
    responses={404: {"description": "Not found"}},
)

@router_user_model.get("/all/",
                        summary="Get all models available to the user",
                        )
async def get_user_models(
    authenticated: bool = Depends(check_permission),
):
    if authenticated:
        models = user_model_functions.get_user_models_by_plan(authenticated["id"])
        if models:
            return models
        else:
            raise HTTPException(status_code=400, detail="No models found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
