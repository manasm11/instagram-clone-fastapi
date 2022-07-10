import json

from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.logger import logger
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from loguru import logger

import auth
import exceptions
from db.database import Base, _engine
from routers import post, user

# Creates Database and Tables
Base.metadata.create_all(_engine)
app = FastAPI()
logger.add(
    "logs/info/info_{time}.log",
    level="INFO",
    rotation="1 month",
    retention="500 days",
    compression="gz",
)

logger.add(
    "logs/debug/debug_{time}.log",
    level="DEBUG",
    rotation="00:00",
    retention="1 week",
)

logger.add(
    "logs/error/error_{time}.log",
    level="ERROR",
    rotation="365 days",
    compression="gz",
)
app.include_router(auth.router)
app.include_router(user.router)
app.include_router(post.router)
app.mount("/images", StaticFiles(directory="images"), name="images")


@app.get("/")
def root():
    return {"message": "API is running. Navigate to /docs to see the documentation."}


app.add_exception_handler(exceptions.UserExists, exceptions.user_exists)
app.add_exception_handler(
    exceptions.InvalidImageExtension, exceptions.invalid_image_extension
)
app.add_exception_handler(exceptions.UserNotExists, exceptions.user_not_exists)
app.add_exception_handler(
    exceptions.MultipleUsersWithSameUsername,
    exceptions.multiple_users_with_same_username,
)
app.add_exception_handler(exceptions.IncorrectPassword, exceptions.incorrect_password)
app.add_exception_handler(exceptions.PostNotExists, exceptions.post_not_exists)
app.add_exception_handler(exceptions.NotAuthorized, exceptions.not_authorized)


origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
