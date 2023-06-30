from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Folder(BaseModel):
    owner: str
    Users: list = []
    name: str
    description: str = None
    is_public: bool = False
    is_active: bool = True
    images: list = []
    tags: list = []
    class Config:
        schema_extra = {
            "example": {
                "owner": "user",
                "Users": ["user1", "user2"],
                "name": "collection",
                "description": "description",
                "is_public": True,
                "is_active": True,
                "images": ["image1", "image2"],
                "tags": ["tag1", "tag2"]
            }
        }

    class Index:
        indexes = {

        }