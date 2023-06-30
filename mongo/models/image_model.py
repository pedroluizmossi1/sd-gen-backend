from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Image(BaseModel):
    image: bytes
    owner: str
    name: str
    description: str = None
    is_public: bool = False
    tags: list = []
    info: dict = {}
    class Config:
        schema_extra = {
            "example": {
                "image": "image",
                "owner": "user",
                "name": "image",
                "description": "description",
                "is_public": True,
                "tags": ["tag1", "tag2"],
                "info": {"info1": "info1", "info2": "info2"}
            }
        }

    class Index:
        indexes = {

        } 