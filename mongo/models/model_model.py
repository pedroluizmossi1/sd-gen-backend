from pydantic import BaseModel, Field, constr, ValidationError, validator

class Model(BaseModel):
    name: constr(min_length=3, max_length=50) = Field(..., description="The name of the model.")
    description: str = None 
    path: constr(min_length=3, max_length=100) = Field(..., description="The path of the model.")
    is_public: bool = True
    is_active: bool = True
    tags: list = []
    info: object = {}
    type: str = None
    version: str = None
    image: bytes = None

    class Config:
        schema_extra = {
            "example": {
                "name": "image",
                "description": "description",
                "path": "folder\\model.type",
                "is_public": True,
                "is_active": True,
                "tags": ["tag1", "tag2"],
                "info": {"info1": "info1", "info2": "info2"},
                "type": "txt2img",
                "version": "SDXL",
                "image": "image"
            }
        }

    class Index:
        indexes = [
            [("path", 'unique'),
        ]
        ]
