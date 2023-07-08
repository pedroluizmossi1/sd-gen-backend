from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Role(BaseModel):
    name: constr(min_length=3, max_length=20)
    description: constr(min_length=3, max_length=50)
    permissions: list = []

    class UpdatePermission(BaseModel):
        permissions: list = []

        class Config:
            schema_extra = {
                "example": {
                    "permissions": ["permission1", "permission2"]
                }
            }

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