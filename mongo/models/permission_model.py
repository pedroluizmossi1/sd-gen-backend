from pydantic import BaseModel, Field, constr, ValidationError, validator

class Permission(BaseModel):
    name: str
    resource: str
    method: str
    description: str = None

    class Config:
        schema_extra = {
            "example": {
                "name": "permission",
                "resource": "resource",
                "method": "method",
                "description": "description"
            }
        }

    class Index:
        indexes = [
            [("name", 'unique')]
        ]