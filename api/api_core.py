import logging
import os

from fastapi import Depends, FastAPI, HTTPException, Request, Response, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.staticfiles import StaticFiles

from config_core import get_config

from .api_auth import router_auth as router_auth
from .api_folders import router_collection as router_collection
from .api_models import router_model as router_model
from .api_plans import router_plan as router_plan
from .api_roles import router_role as router_role
from .api_users import router_user as router_user
from .api_users_folder import router_user_folder as router_user_folder
from .api_users_images import router_user_image as router_user_image
from .api_users_model import router_user_model as router_user_model
#from .utils import PrometheusMiddleware, metrics, setting_otlp

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

APP_NAME = os.environ.get("APP_NAME", "app")
OTLP_GRPC_ENDPOINT = "http://localhost:4317"
#app.add_middleware(PrometheusMiddleware, app_name="app")
#app.add_route("/metrics", metrics)




class EndpointFilter(logging.Filter):
    # Uvicorn endpoint access log filter
    def filter(self, record: logging.LogRecord) -> bool:
        return record.getMessage().find("GET /metrics") == -1


# Filter out /endpoint
logging.getLogger("uvicorn.access").addFilter(EndpointFilter())

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
app.include_router(router_user_folder)
app.include_router(router_user_model)
app.include_router(router_user_image)
app.include_router(router_role)
app.include_router(router_plan)
app.include_router(router_model)

