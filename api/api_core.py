from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from .api_auth import router_auth as router_auth
from .api_collections import router_collection as router_collection
from .api_users import router_user as router_user

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


@app.get("/")
async def root():
    return {"message": "Hello World"}

