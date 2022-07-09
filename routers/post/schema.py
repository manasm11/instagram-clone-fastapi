import re
from datetime import datetime
from enum import Enum
from typing import Any, List

from pydantic import BaseModel, Field, validator

from db.database import get_db
from db.models import DbUser


class PostRequest(BaseModel):
    image_url: Any = Field(
        ..., description="Image URL", example="https://example.com/img.jpg"
    )
    caption: Any = Field(..., description="Caption", example="This is a caption")
    creator_id: Any = Field(..., description="Creator ID", example=1)

    @validator("image_url")
    def image_url_validate(cls, v):
        if v is None:
            raise ValueError("Image URL missing")
        if not re.match(
            "(?:(?:http//|https://)|/)[^\"']*.(?:png|jpg|jpeg|gif|png|svg)", v
        ):
            raise ValueError(f"Image URL is not valid: '{v}'")
        return v

    @validator("caption")
    def caption_validate(cls, v):
        if v is None:
            raise ValueError("Caption missing")
        return v

    @validator("creator_id")
    def creator_id_validate(cls, v):
        if v is None:
            raise ValueError("Creator missing")
        if str(v).isdecimal() is False:
            raise ValueError("Creator Id incorrect")
        v = int(v)
        if not next(get_db()).query(DbUser).get(v):
            raise ValueError("Creator (User) does not exist")
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


class PostListResponse(BaseModel):
    posts: List[PostResponse]
