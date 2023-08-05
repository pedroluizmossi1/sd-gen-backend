from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator
from datetime import date, datetime, time, timedelta
from functions_core import get_config
import time

name_regex = "^[a-zA-ZÀ-ÿ0-9_\s.]+$"
login_regex = "^[a-zA-Z0-9_-]+$"

user_settings = {
    "dark_mode": False
}


class User(BaseModel):
    login: constr(min_length=3, max_length=20, regex=login_regex)
    password: str
    email: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
    first_name: constr(min_length=3, max_length=50, regex=name_regex) = None
    last_name: constr(min_length=3, max_length=50, regex=name_regex) = None
    is_active: bool = False
    role: object = None
    plan: object = None
    folders: list = []
    settings: object = user_settings
    profile_picture: bytes = None
    created_at: datetime = None
    updated_at: datetime = None
    last_login: datetime = None
    last_logout: datetime = None
    last_password_change: datetime = None
    
    @validator('created_at', 'updated_at', pre=True, always=True)
    def set_created_at(cls, v):
        return v or datetime.utcnow()
    
    class Login(BaseModel):
        login: constr(min_length=3, max_length=20, regex=login_regex)
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
        login: constr(min_length=3, max_length=20, regex=login_regex)
        password: constr(min_length=3, max_length=50)
        email: constr(min_length=3, max_length=50, regex="^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        first_name: constr(min_length=3, max_length=50, regex=name_regex)
        last_name: constr(min_length=3, max_length=50, regex=name_regex)

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
        first_name: constr(min_length=3, max_length=50, regex=name_regex)
        last_name: constr(min_length=3, max_length=50, regex=name_regex)

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