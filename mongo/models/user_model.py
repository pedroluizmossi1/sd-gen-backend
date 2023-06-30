from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class User(BaseModel):
    login: constr(min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")
    password: str
    email: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    first_name: str = None
    last_name: str = None
    is_active: bool = False
    role = str = "null"
    plan = str = "null"

    class Login(BaseModel):
        login: str
        password: str

    class Logout(BaseModel):
        login: str = Field(None, alias='login')

    class UserInsert(BaseModel):
        login: str
        password: str
        email: str
        first_name: str = None
        last_name: str = None

    class UserUpdate(BaseModel):
        email: str
        first_name: str = None
        last_name: str = None

    class Config:
        schema_extra = {
            "example": {
                "login": "user",
                "password": "password",
                "email": "user@email.com",
                "first_name": "first_name",
                "last_name": "last_name",
                "is_active": True
            }
        }
    class Index:
        indexes = [
            [("login", 'unique'),
            ("email", 'unique')]

        ]