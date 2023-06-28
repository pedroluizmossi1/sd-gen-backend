from pydantic import BaseModel, Field, constr, validate_model, ValidationError, validator
from typing import Optional, List, Dict, Any
from bson import ObjectId
import re
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
        token: str
        user: str

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

class Folder(BaseModel):
    owner: str
    Users: list = []
    name: str
    description: str = None
    is_public: bool = False
    is_active: bool = True
    images: list = []
    tags: list = []
    class Config:
        schema_extra = {
            "example": {
                "owner": "user",
                "Users": ["user1", "user2"],
                "name": "collection",
                "description": "description",
                "is_public": True,
                "is_active": True,
                "images": ["image1", "image2"],
                "tags": ["tag1", "tag2"]
            }
        }

    class Index:
        indexes = {

        }

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
