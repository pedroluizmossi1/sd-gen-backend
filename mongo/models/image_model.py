from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Image(BaseModel):
    owner: bytes
    name: str
    description: str = None
    is_public: bool = False
    tags: list = []
    info: dict = {}
    type: str = "txt2img"
    image: bytes
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
        

    class Index:
        indexes = {

        } 