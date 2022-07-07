import json

from fastapi import FastAPI, Request, Response
from fastapi.logger import logger
from fastapi.responses import JSONResponse, StreamingResponse
from loguru import logger

import exceptions
from db.database import Base, _engine
from routers import user

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
app.include_router(user.router)


@app.get("/")
def root():
    return {"message": "API is running"}


app.add_exception_handler(exceptions.UserExists, exceptions.user_exists)
