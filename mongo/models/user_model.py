from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator

class User(BaseModel):
    login: constr(min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")
    password: str
    email: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    first_name: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$") = None
    last_name: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$") = None
    is_active: bool = False
    role: object = None
    plan: object = None
    
    class Login(BaseModel):
        login: constr(min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")
        password: str = 'Password'

        class Config:
            schema_extra = {
                "example": {
                    "login": "user",
                    "password": "password"
                }
            }

    class Logout(BaseModel):
        login: str = Field(None, alias='login')

    class UserInsert(BaseModel):
        login: constr(min_length=3, max_length=20, regex="^[a-zA-Z0-9_-]+$")
        password: str
        email: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        first_name: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")
        last_name: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")

        class Config:
            schema_extra = {
                "example": {
                    "login": "user",
                    "password": "password",
                    "email": "user@user.com",
                    "first_name": "first_name",
                    "last_name": "last_name"
                }
            }        
    
    class UpdateFirstLastName(BaseModel):
        first_name: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")
        last_name: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_-]+$")

        class Config:
            schema_extra = {
                "example": {
                    "first_name": "first_name",
                    "last_name": "last_name"
                }
            }

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