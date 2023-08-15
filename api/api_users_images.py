import random
from typing import Optional
import httpx
from fastapi import APIRouter, Depends, HTTPException, Response
from pydantic import ValidationError, validate_model
import api.api_users_folder as api_users_folder
import mongo.functions.user_image_functions as user_image_functions
import mongo.functions.folder_functions as folder_functions
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


SDXL_SERVER = 0
SD15_SERVER = 1


@router_user_image.get("/")
async def get_user_image(
    image_id: str,
    authenticated: bool = Depends(check_permission),
):
    """Get user image by id"""
    try:
        if authenticated["permission"] is True:
            image = user_image_functions.get_image(
                image_id, authenticated["id"])
            if image:
                return Response(content=image["image"], media_type="image/webp")
            else:
                raise HTTPException(status_code=400, detail="Image not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router_user_image.delete("/")
async def delete_user_image(
    image_id: str,
    authenticated: bool = Depends(check_permission),
):
    """Delete user image by id"""
    try:
        if authenticated["permission"] is True:
            image = user_image_functions.delete_image(
                image_id, authenticated["id"])
            if image:
                return {"message": "Image deleted"}
            else:
                raise HTTPException(status_code=400, detail="Image not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router_user_image.post("/txt2img/v2/sdxl/")
async def create_user_image_txt2img_v2_sdxl(
        image: image_model.Image.Txt2ImgV2Sdxl,
        folder: Optional[str] = "root",
        refiner: Optional[bool] = False,
        authenticated: bool = Depends(check_permission)):
    """Create user image from text using SDXL"""
    try:
        if authenticated["permission"] is True:
            image_list = []
            image_insert = image_model.Image(owner=authenticated["id"], name=f"txt2img_{random.randint(100000, 999999)}", description="Image generated from text",
                                             tags=["txt2img"], info={}, type="txt2img", image="")
            response = folder_functions.get_folder_by_name(
                folder, authenticated["id"])
            if response:
                plan_resource = check_plan(
                    ["SDXL_X", "SDXL_Y", "BATCH_SIZE", "SDXL_SAMPLER", "STEPS", "SDXL", "REFINER"], authenticated["plan"])
                if image.height <= plan_resource["SDXL_X"] and image.width <= plan_resource["SDXL_Y"] and image.batch_size <= plan_resource["BATCH_SIZE"] and image.sampler_name in plan_resource["SDXL_SAMPLER"] and image.steps <= plan_resource["STEPS"] and plan_resource["SDXL"] is True:
                    if refiner and plan_resource["REFINER"] is True:
                        prompt_config = comfy_sdxl.sdxl_refiner_exporter(image.prompt, image.negative_prompt, image.seed, image.refiner_seed, image.refiner_denoise,
                                                                         image.width, image.height, image.batch_size, image.model_path, image.steps, image.cfg_scale, image.sampler_name)
                    else:
                        prompt_config = comfy_sdxl.sdxl_exporter(image.prompt, image.negative_prompt, image.seed, image.width,
                                                                 image.height, image.batch_size, image.model_path, image.steps, image.cfg_scale, image.sampler_name)
                    response = await comfy_core.async_get_images(prompt_config, authenticated['id'], SDXL_SERVER)
                    images_process_list = process_images_multithread_bytes(
                        response)
                    for key in images_process_list:
                        image_insert.image = key
                        inserted_image = user_image_functions.create_image(
                            image_insert, folder, authenticated["id"])
                        if inserted_image:
                            image_list.append(inserted_image)
                        else:
                            raise HTTPException(
                                status_code=400, detail="Error creating image")
                    if "error" in response:
                        raise HTTPException(
                            status_code=400, detail=response["error"])
                    else:
                        return {"message": "Image(s) created", "images": image_list}
                else:
                    raise HTTPException(
                        status_code=401, detail="Value higher than allowed by plan")
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router_user_image.get("/txt2img/v2/sdxl/queue/")
async def create_user_image_txt2img_v2_sdxl_queue(
        authenticated: bool = Depends(check_permission)):
    """Get user image queue from SDXL"""	
    try:
        if authenticated:
            return await comfy_core.get_queue_async(authenticated["id"], SDXL_SERVER)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err

@router_user_image.post("/txt2img/v2/sd15/")
async def create_user_image_txt2img_v2_sd15(
        image: image_model.Image.Txt2ImgV2Sd15,
        folder: Optional[str] = "root",
        authenticated: bool = Depends(check_permission),
        latent: Optional[bool] = False):
    """Create user image from text using SD15"""
    try:
        if authenticated["permission"] == True:
            image_list = []
            image_insert = image_model.Image(owner=authenticated["id"], name=f"txt2img_{random.randint(100000, 999999)}", description="Image generated from text",
                                            tags=["txt2img"], info={}, type="txt2img", image="")
            response = folder_functions.get_folder_by_name(
                folder, authenticated["id"])
            if response:
                plan_resource = check_plan(
                    ["BASE_X", "BASE_Y", "BATCH_SIZE", "SD15_SAMPLER", "STEPS", "SD15", "LATENT"], authenticated["plan"])
                if image.height <= plan_resource["BASE_X"] and image.width <= plan_resource["BASE_Y"] and image.batch_size <= plan_resource["BATCH_SIZE"] and image.sampler_name in plan_resource["SD15_SAMPLER"] and image.steps <= plan_resource["STEPS"] and plan_resource["SD15"] is True:
                    
                        if latent and plan_resource["LATENT"] is True:
                            prompt_config = comfy_sd15.sd15_latent_exporter(image.prompt, image.negative_prompt, image.seed, image.width, image.height, image.batch_size,
                                                                            image.model_path, image.steps, image.cfg_scale, image.sampler_name, image.latent_denoise, image.latent_seed,
                                                                            image.latent_steps, image.latent_cfg, image.latent_sampler_name)
                        else:
                            prompt_config = comfy_sd15.sd15_exporter(image.prompt, image.negative_prompt, image.seed, image.width,
                                                                    image.height, image.batch_size, image.model_path, image.steps, image.cfg_scale, image.sampler_name)
                        response = await comfy_core.async_get_images(prompt_config, authenticated['id'], SD15_SERVER)
                        images_process_list = process_images_multithread_bytes(
                            response)
                        for key in images_process_list:
                            image_insert.image = key
                            inserted_image = user_image_functions.create_image(
                                image_insert, folder, authenticated["id"])
                            if inserted_image:
                                image_list.append(inserted_image)
                            else:
                                raise HTTPException(
                                    status_code=400, detail="Error creating image")
                        if "error" in response:
                            raise HTTPException(
                                status_code=400, detail=response["error"])
                        else:
                            return {"message": "Image(s) created", "images": image_list}
                else:
                    raise HTTPException(
                        status_code=401, detail="Value higher than allowed by plan")
            else:
                raise HTTPException(status_code=400, detail="Folder not found")
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err


@router_user_image.get("/txt2img/v2/sd15/queue/")
async def create_user_image_txt2img_v2_sd15_queue(
    authenticated: bool = Depends(check_permission),
):
    """Get queue of images to be processed"""	
    try:
        if authenticated:
            return await comfy_core.get_queue_async(authenticated["id"], SD15_SERVER)
        else:
            raise HTTPException(status_code=401, detail="Unauthorized")
    except Exception as err:
        raise HTTPException(status_code=500, detail=str(err)) from err