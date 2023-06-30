from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Permission(BaseModel):
    name: str
    resource: str
    description: str = None

    class Config:
        schema_extra = {
            "example": {
                "name": "permission",
                "resource": "resource",
                "description": "description"
            }
        }

    class Index:
        indexes = [
            [("name", 'unique')]
        ]