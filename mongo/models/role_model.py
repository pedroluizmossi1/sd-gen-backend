from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Role(BaseModel):
    name: str
    description: str = None
    permissions: list = []

    class Config:
        schema_extra = {
            "example": {
                "name": "role",
                "description": "description",
                "permissions": ["permission1", "permission2"]
            }  
        }

    class Index:
        indexes = [
            [("name", 'unique')]
        ]