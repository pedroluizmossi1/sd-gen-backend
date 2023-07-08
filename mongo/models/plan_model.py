from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Plan(BaseModel):
    name: constr(min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")
    description: constr(min_length=3, max_length=50)
    price: int = 0
    resources: list = []

    class Update(BaseModel):
        description: constr(min_length=3, max_length=50) = None
        price: int = None

        class Config:
            schema_extra = {
                "example": {
                    "description": "description",
                    "price": 0
                }
            }

    class UpdateResources(BaseModel):
        resources: list = []

        class Config:
            schema_extra = {
                "example": {
                    "resources": [{"resource1": "resource1"}, {"resource2": "resource2"}]
                }
            }
    class Config:
        schema_extra = {
            "example": {
                "name": "plan",
                "description": "description",
                "price": 0,
                "resources": [{"resource1": "resource1"}, {"resource2": "resource2"}]
            }
        }

    class Index:
        indexes = [
            [("name", 'unique')]
        ]