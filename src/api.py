import asyncio
from contextlib import asynccontextmanager
from fastapi import APIRouter, FastAPI

from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sqlalchemy import String

from src.config.settings import Settings
from src.routes import routers
from src.config.database import get_session

from alembic.config import Config
from alembic import command




@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Started the app...")
    print(f"Loaded settings: {Settings().model_dump()}")
    app.state.async_session = get_session()
    yield
    print("Closing in...")
    await app.state.async_session.aclose()

app = FastAPI(lifespan=lifespan)


# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173"
    ],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


   

for name, obj in vars(routers).items():
    if isinstance(obj, APIRouter):  # Check if it's a valid APIRouter object
        app.include_router(obj)
        print(f"Included router: {obj.prefix}")


""" app.mount(
    "/files",
    StaticFiles(directory="uploads"),
    name="uploads",
)
 """

app.mount(
    "/static/images",
    StaticFiles(directory="uploads"),
    name="uploads",
)


@app.get("/", tags=["Root"])
async def index():
    string_python_type = String()
    print(string_python_type)  # <class 'str'>
    return {
        "message": "Hi, We're Mohamed & Chirine. Awesome - Our set up is done & working."
    }
