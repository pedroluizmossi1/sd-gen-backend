from fastapi import FastAPI, Depends, Request, Response, status, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.openapi.docs import get_swagger_ui_html
from .api_auth import router_auth as router_auth
from .api_folders import router_collection as router_collection
from .api_users import router_user as router_user
from .api_roles import router_role as router_role
from config_core import get_config
import os

app = FastAPI()
origins = [
    "http://192.168.100.44:8100",
    "http://localhost:8100",
    "http://localhost",
    "http://localhost:8000",
    # all origins
    "*"
    # Add other origins that are allowed to access your API
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    
)

app.include_router(router_auth)
app.include_router(router_collection)
app.include_router(router_user)
app.include_router(router_role)

app.mount("/static", StaticFiles(directory="static"), name="static")

