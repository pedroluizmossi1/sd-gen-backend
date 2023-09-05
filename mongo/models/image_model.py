from pydantic import BaseModel, Field, constr, ValidationError, validator

class Image(BaseModel):
    owner: bytes
    name: str
    description: str = None
    is_public: bool = False
    tags: list = []
    info: dict = {}
    type: str = "txt2img"
    image: bytes
    created_at: str = None
    updated_at: str = None
    class Config:
        schema_extra = {
            "example": {
                "owner": "user",
                "name": "image",
                "description": "description",
                "is_public": True,
                "tags": ["tag1", "tag2"],
                "info": {"info1": "info1", "info2": "info2"},
                "type": "txt2img",
                "image": "image"
            }
        }

    class Insert(BaseModel):
        name: str
        description: str = None
        is_public: bool = False
        tags: list = []
        info: dict = {}
        image: bytes
        class Config:
            schema_extra = {
                "example": {
                    "name": "image",
                    "description": "description",
                    "is_public": True,
                    "tags": ["tag1", "tag2"],
                    "info": {"info1": "info1", "info2": "info2"},
                    "type": "txt2img",
                    "image": "image"
                }
            }

    class Txt2Img(BaseModel):
        prompt: str
        seed: int = -1
        sampler_name: str = "Euler a"
        batch_size: int = 1
        steps: int = 20
        cfg_scale: float = 7.0
        width: int = 512
        height: int = 512
        send_image: bool = True

        class Config:
            schema_extra = {
                "example": {
                    "prompt": "prompt",
                    "seed": -1,
                    "sampler_name": "Euler a",
                    "batch_size": 1,
                    "steps": 20,
                    "cfg_scale": 7.0,
                    "width": 512,
                    "height": 512,
                    "send_image": True
                }
            }

    class Txt2ImgV2Sdxl(BaseModel):
        prompt: str
        negative_prompt: str = None
        seed: int = -1
        refiner_seed: int = -1
        refiner_denoise: float = 0.1
        batch_size: int = 1
        width: int = 1024
        height: int = 1024,
        steps: int = 15
        cfg_scale: float = 7.0
        sampler_name: str = "dpmpp_2m"
        model_path: str = None
        send_image: bool = True

        class Config:
            schema_extra = {
                "example": {
                    "prompt": "dog surfing, beach island, anime style, close view, water splash drops",
                    "negative_prompt": "(low quality:1.3) (((3D render)))",
                    "seed": -1,
                    "refiner_seed": -1,
                    "refiner_denoise": 0.1,
                    "batch_size": 1,
                    "width": 1024,
                    "height": 1024,
                    "steps": 15,
                    "cfg_scale": 7.0,
                    "sampler_name": "dpmpp_2m",
                    "model_path": "SDXL\\dreamshaperXL10_alpha2Xl10.safetensors",
                    "send_image": True
                }
            }

    class Txt2ImgV2Sd15(BaseModel):
        prompt: str
        negative_prompt: str = None
        seed: int = -1
        batch_size: int = 1
        width: int = 512
        height: int = 768,
        steps: int = 20
        cfg_scale: float = 7.0
        sampler_name: str = "euler"
        model_path: str = None
        latent_seed: int = -1
        latent_denoise: float = 0.5
        latent_steps: int = 20
        latent_cfg: float = 7.0
        latent_sampler_name: str = "euler"
        send_image: bool = True

        class Config:
            schema_extra = {
                "example": {
                    "prompt": "dog surfing, beach island, anime style, close view, water splash drops",
                    "negative_prompt": "(low quality:1.3) (((3D render)))",
                    "seed": -1,                 
                    "batch_size": 1,
                    "width": 512,
                    "height": 768,
                    "steps": 20,                
                    "cfg_scale": 7.0,                 
                    "sampler_name": "euler",
                    "model_path": "Artistic\\dreamshaper_8.safetensors",
                    "latent_seed": -1,
                    "latent_denoise": 0.5,
                    "latent_steps": 20,
                    "latent_cfg": 7.0,
                    "latent_sampler_name": "euler",
                    "send_image": True
                }
            }
        
    class faceSwapImg(BaseModel):
        image: bytes
        class Config:
            schema_extra = {
                "example": {
                    "image": "data:image/jpeg;base64,/9j/4AAQSkZJRgABA..."
                }
            }
    
    class faceSwap(BaseModel):
        target_id: str = None
        reference_id: str = None
        target_url: str = None
        reference_url: str = None
        upscale: bool = True
        face_index: int = 0
        class Config:
            schema_extra = {
                "example": {
                    "target_id": "",
                    "reference_id": "",
                    "target_url": "",
                    "reference_url": "",
                    "upscale": True,
                    "face_index": 0
                }
            }
    class Index:
        indexes = {

        } 