from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Folder(BaseModel):
    owner: object = None
    name: constr(min_length=3, max_length=50)
    description: constr(min_length=3, max_length=100) = None
    is_public: bool = False
    is_active: bool = True
    images: list = []
    tags: list = []
    class Config:
        schema_extra = {
            "example": {
                "owner": "user",
                "name": "collection",
                "description": "description",
                "is_public": False,
                "is_active": True,
                "images": ["image1", "image2"],
                "tags": ["tag1", "tag2"],
                "folders": ["folder1", "folder2"]
            }
        }

    class Insert(BaseModel):
        name: constr(min_length=3, max_length=50)
        description: constr(min_length=3, max_length=100) = None
        is_public: bool = False
        tags: list = []
        class Config:
            schema_extra = {
                "example": {
                    "name": "collection",
                    "description": "description",
                    "is_public": False,
                    "tags": ["tag1", "tag2"]
                }
            }

    class Update(BaseModel):
        description: constr(min_length=3, max_length=100) = None
        is_public: bool = False
        is_active: bool = True
        tags: list = []
        class Config:
            schema_extra = {
                "example": {
                    "name": "collection",
                    "description": "description",
                    "is_public": False,
                    "is_active": True,
                    "tags": ["tag1", "tag2"]
                }
            }


    class Index:
        indexes = {

    }
            