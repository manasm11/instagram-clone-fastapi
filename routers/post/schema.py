import re
from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field, validator

from db.database import get_db
from db.models import DbUser


class PostRequest(BaseModel):
    image_url: Any
    image_url_type: Any
    caption: Any
    creator_id: Any

    @validator("image_url")
    def validate_image_url(cls, v):
        if v is None:
            raise ValueError("Image URL missing")
        if not re.match("(http)?s?:?(\/\/[^\"']*\.(?:png|jpg|jpeg|gif|png|svg))", v):
            raise ValueError("Image URL is not valid")
        return v

    @validator("caption")
    def validate_caption(cls, v):
        if v is None:
            raise ValueError("Caption missing")
        return v

    @validator("creator_id")
    def validate_creator_id(cls, v):
        if v is None:
            raise ValueError("Creator missing")
        if str(v).isdecimal() is False:
            raise ValueError("Creator Id incorrect")
        v = int(v)
        if not next(get_db()).query(DbUser).get(v):
            raise ValueError("Creator (User) does not exist")
        return v

    @validator("image_url_type")
    def validate_image_url_type(cls, v):
        if v is None:
            raise ValueError("Image URL Type missing")
        if v not in ["absolute", "relative"]:
            raise ValueError("Image URL Type must be 'absolute' or 'relative'")
        return v


class UserInPostResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int
    image_url: str
    image_url_type: str
    caption: str
    timestamp: datetime
    creator: UserInPostResponse

    class Config:
        orm_mode = True
