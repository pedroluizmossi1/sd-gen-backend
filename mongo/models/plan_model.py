from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class Plan(BaseModel):
    name: str
    description: str = None
    price: int
    resources: dict = {}

    class Config:
        schema_extra = {
            "example": {
                "name": "plan",
                "description": "description",
                "price": 0,
                "resources": {"resource1": "resource1", "resource2": "resource2"}
            }
        }

    class Index:
        indexes = [
            [("name", 'unique')]
        ]