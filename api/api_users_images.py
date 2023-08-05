import asyncio
import random
from typing import Optional

import httpx
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import ValidationError, validate_model

import api.api_users_folder as api_users_folder
import mongo.functions.user_image_functions as user_image_functions
import mongo.models.image_model as image_model
import sd_automatic.automatic_core as automatic_core
import sd_comfy.comfy_core as comfy_core
import sd_comfy.comfy_sd15 as comfy_sd15
import sd_comfy.comfy_sdxl as comfy_sdxl
from config_core import get_config
from functions_core import (process_image, process_images_multithread,
                            process_images_multithread_bytes)

from .api_auth import authorize_token, check_permission, check_plan

router_user_image = APIRouter(
    prefix="/user/image",
    tags=["User Image"],
    responses={404: {"description": "Not found"}},
)

fastapi_endpoint_url = get_config("FASTAPI", "fastapi_endpoint_url")


sdxl_server = 0
sd15_server = 1

@router_user_image.get("/")
async def get_user_image(
    image_id: str,
    authenticated: bool = Depends(check_permission),
):
    if authenticated["permission"] == True:
        try:
            image = user_image_functions.get_image(image_id, authenticated["id"])
            if image:
                return Response(content=image["image"], media_type="image/webp")
            else:
                raise HTTPException(status_code=400, detail="Image not found")
        except Exception as e:
            raise HTTPException(status_code=500,detail="Image not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router_user_image.delete("/")
async def delete_user_image(
    image_id: str,
    authenticated: bool = Depends(check_permission),
):
    if authenticated["permission"] == True:
        try:
            image = user_image_functions.delete_image(image_id, authenticated["id"])
            if image:
                return {"message": "Image deleted"}
            else:
                raise HTTPException(status_code=400, detail="Image not found")
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")

@router_user_image.post("/txt2img/", deprecated=True)
async def create_user_image_txt2img(
    image: image_model.Image.Txt2Img,
    folder: Optional[str] = "root",
    authenticated: bool = Depends(check_permission)
):  
    if authenticated["permission"] == True:
        image_list = []
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
            response = await client.get(
                f"{fastapi_endpoint_url}/user/folder/get/",
                params={"id_or_folder": folder},
                headers={"Authorization": authenticated['token']},
            )
            
            if response.status_code == 200:
                if authenticated:
                    plan_resource = check_plan(["BASE_X","BASE_Y", "STEPS", "BATCH_SIZE"], authenticated["plan"])
                    if image.height <= plan_resource["BASE_X"] and image.width <= plan_resource["BASE_Y"] and image.steps <= plan_resource["STEPS"] and image.batch_size <= plan_resource["BATCH_SIZE"]:
                        try:
                            response = automatic_core.create_user_image_txt2img(image)
                            images_process_list = process_images_multithread(response["images"])
                            for key in images_process_list:
                                image_insert.image = key
                                inserted_image = user_image_functions.create_image(image_insert, folder, authenticated["id"])
                                if inserted_image:
                                    image_list.append(inserted_image)
                                else:
                                    raise HTTPException(status_code=400, detail="Error creating image")
                            if "error" in response:
                                raise HTTPException(status_code=400, detail=response["error"])
                            else:
                                return {"message": "Image(s) created", "images": image_list}
                        except Exception as e:
                            raise HTTPException(status_code=500, detail=str(e))   
                    else:
                        raise HTTPException(status_code=401, detail="Value higher than allowed by plan")
                else:
                    raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    

@router_user_image.post("/txt2img/v2/sdxl/")
async def create_user_image_txt2img_v2_sdxl(
    image: image_model.Image.Txt2ImgV2Sdxl,
    folder: Optional[str] = "root",
    refiner: Optional[bool] = False,
    authenticated: bool = Depends(check_permission)):  
    if authenticated["permission"] == True:
        image_list = []
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
            response = await client.get(
                f"{fastapi_endpoint_url}/user/folder/get/",
                params={"id_or_folder": folder},
                headers={"Authorization": authenticated['token']},
            )

            if response.status_code == 200:
                if authenticated:
                    plan_resource = check_plan(["BASE_X","BASE_Y", "BATCH_SIZE"], authenticated["plan"])
                    if image.height <= plan_resource["BASE_X"] and image.width <= plan_resource["BASE_Y"] and image.batch_size <= plan_resource["BATCH_SIZE"]:
                        try:
                            if refiner:
                                prompt_config = comfy_sdxl.sdxl_refiner_exporter(image.prompt, image.negative_prompt, image.seed, image.refiner_seed, image.refiner_denoise, image.width, image.height, image.batch_size, image.model_path, image.steps,image.cfg_scale, image.sampler_name)
                            else:
                                prompt_config = comfy_sdxl.sdxl_exporter(image.prompt, image.negative_prompt, image.seed, image.width, image.height, image.batch_size, image.model_path, image.steps,image.cfg_scale, image.sampler_name)
                            response = await comfy_core.async_get_images(prompt_config, authenticated['id'], sdxl_server)
                            images_process_list = process_images_multithread_bytes(response)
                            for key in images_process_list:
                                image_insert.image = key
                                inserted_image = user_image_functions.create_image(image_insert, folder, authenticated["id"])
                                if inserted_image:
                                    image_list.append(inserted_image)
                                else:
                                    raise HTTPException(status_code=400, detail="Error creating image")
                            if "error" in response:
                                raise HTTPException(status_code=400, detail=response["error"])
                            else:
                                return {"message": "Image(s) created", "images": image_list}
                        except Exception as e:
                            raise HTTPException(status_code=500, detail=str(e))
                    else:
                        raise HTTPException(status_code=401, detail="Value higher than allowed by plan")
                else:
                    raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
        
@router_user_image.get("/txt2img/v2/sdxl/queue/")
async def create_user_image_txt2img_v2_sdxl_queue(
    authenticated: bool = Depends(check_permission)):
    if authenticated:
        return await comfy_core.get_queue_async(authenticated["id"], sdxl_server)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user_image.post("/txt2img/v2/sd15/")
async def create_user_image_txt2img_v2_sd15(
    image: image_model.Image.Txt2ImgV2Sd15,
    folder: Optional[str] = "root",
    authenticated: bool = Depends(check_permission),
    latent: Optional[bool] = False):  
    if authenticated["permission"] == True:
        image_list = []
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
            response = await client.get(
                f"{fastapi_endpoint_url}/user/folder/get/",
                params={"id_or_folder": folder},
                headers={"Authorization": authenticated['token']},
            )

            if response.status_code == 200:
                if authenticated:
                    plan_resource = check_plan(["BASE_X","BASE_Y", "BATCH_SIZE"], authenticated["plan"])
                    if image.height <= plan_resource["BASE_X"] and image.width <= plan_resource["BASE_Y"] and image.batch_size <= plan_resource["BATCH_SIZE"]:
                        #try:
                            if latent:
                                prompt_config = comfy_sd15.sd15_latent_exporter(image.prompt, image.negative_prompt, image.seed, image.width, image.height, image.batch_size,
                                                                                image.model_path, image.steps,image.cfg_scale, image.sampler_name, image.latent_denoise, image.latent_seed,
                                                                                image.latent_steps, image.latent_cfg, image.latent_sampler_name)
                            else:
                                prompt_config = comfy_sd15.sd15_exporter(image.prompt, image.negative_prompt, image.seed, image.width, image.height, image.batch_size, image.model_path, image.steps,image.cfg_scale, image.sampler_name)
                            response = await comfy_core.async_get_images(prompt_config, authenticated['id'], sd15_server)
                            images_process_list = process_images_multithread_bytes(response)
                            for key in images_process_list:
                                image_insert.image = key
                                inserted_image = user_image_functions.create_image(image_insert, folder, authenticated["id"])
                                if inserted_image:
                                    image_list.append(inserted_image)
                                else:
                                    raise HTTPException(status_code=400, detail="Error creating image")
                            if "error" in response:
                                raise HTTPException(status_code=400, detail=response["error"])
                            else:
                                return {"message": "Image(s) created", "images": image_list}
                        #except Exception as e:
                            #raise HTTPException(status_code=500, detail=str(e))
                    else:
                        raise HTTPException(status_code=401, detail="Value higher than allowed by plan")
                else:
                    raise HTTPException(status_code=401, detail="Unauthorized")
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")
    
@router_user_image.get("/txt2img/v2/sd15/queue/")
async def create_user_image_txt2img_v2_sd15_queue(
    authenticated: bool = Depends(check_permission),
):
    if authenticated:
        return await comfy_core.get_queue_async(authenticated["id"], sd15_server)
    else:
        raise HTTPException(status_code=401, detail="Unauthorized")