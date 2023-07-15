from fastapi import APIRouter, Depends, HTTPException
import requests
import mongo.models.image_model as image_model
import mongo.functions.user_image_functions as user_image_functions
import api.api_users_folder as api_users_folder
import sd_automatic.automatic_core as automatic_core
from config_core import get_config
from .api_auth import authorize_token, check_permission, check_plan
from pydantic import validate_model, ValidationError
from typing import Optional
import random
import httpx

router_user_image = APIRouter(
    prefix="/user/image",
    tags=["User Image"],
    responses={404: {"description": "Not found"}},
)

fastapi_endpoint_url = get_config("FASTAPI", "fastapi_endpoint_url")

@router_user_image.post("/txt2img")
async def create_user_image_txt2img(
    image: image_model.Image.Txt2Img,
    folder: Optional[str] = "/",
    authenticated: bool = Depends(check_permission),
):  
    image_insert =  image_model.Image(
                                    owner = authenticated["id"],
                                    name = f"txt2img_{random.randint(100000, 999999)}",
                                    description = "Image generated from text",
                                    tags = ["txt2img"],
                                    info = {},
                                    type = "txt2img",
                                    image = ""
                                    )
    async with httpx.AsyncClient() as client:
        print(authenticated['token'])
        response = await client.get(
            f"{fastapi_endpoint_url}/user/folder/get/",
            params={"id_or_folder": "root"},
            headers={"Authorization": authenticated['token']},
        )
        if response.status_code == 200:
            if authenticated:
                plan_resource = check_plan(["BASE_X","BASE_Y", "STEPS", "BATCH_SIZE"], authenticated["plan"])
                if image.height <= plan_resource["BASE_X"] and image.width <= plan_resource["BASE_Y"] and image.steps <= plan_resource["STEPS"] and image.batch_size <= plan_resource["BATCH_SIZE"]:
                    try:
                        response = automatic_core.create_user_image_txt2img(image)
                        image_count = len(response["images"])
                        for key in response["images"]:
                            image_insert.image = key
                            if user_image_functions.create_image(image_insert, folder, authenticated["id"]):
                               pass 
                            else:
                                raise HTTPException(status_code=400, detail="Error creating image")
                        if "error" in response:
                            raise HTTPException(status_code=400, detail=response["error"])
                        else:
                            return {"status": "Image created", "images": image_count}
                    except Exception as e:
                        raise HTTPException(status_code=400, detail=str(e))
                else:
                    raise HTTPException(status_code=401, detail="Value higher than allowed by plan")
            else:
                raise HTTPException(status_code=401, detail="Unauthorized")
        else:
            raise HTTPException(status_code=400, detail="Folder not found")
        
        
