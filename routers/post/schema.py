import re
from datetime import datetime
from enum import Enum
from typing import Any, List

from pydantic import BaseModel, Field, validator

from db import DbUser, get_db


class PostRequest(BaseModel):
    image_url: Any = Field(
        ..., description="Image URL", example="https://example.com/img.jpg"
    )
    caption: Any = Field(..., description="Caption", example="This is a caption")

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


class CommentRequest(BaseModel):
    # TODO: Add validation for comment
    username: str = Field(..., description="Username", example="test")
    text: str = Field(
        ..., description="Comment", example="This is a comment", min_length=1
    )
    post_id: int = Field(..., description="Post ID", example=1)


class _UserInPostResponse(BaseModel):
    username: str = Field(..., description="Username", example="test")

    class Config:
        orm_mode = True


class _CommentInPostResponse(BaseModel):
    text: str = Field(..., description="Comment", example="This is a comment")
    username: str = Field(..., description="Username", example="test")
    timestamp: datetime = Field(
        ..., description="Creation Timestamp", example=datetime.now()
    )

    class Config:
        orm_mode = True


class PostResponse(BaseModel):
    id: int = Field(..., description="Post ID", example=1)
    image_url: str = Field(
        ..., description="Image URL", example="https://example.com/img.jpg"
    )
    caption: str = Field(..., description="Caption", example="This is a caption")
    timestamp: datetime = Field(
        description="Creation Timestamp", example=datetime.now()
    )
    creator: _UserInPostResponse = Field(
        description="Creator", example=_UserInPostResponse(username="test")
    )

    comments: List[_CommentInPostResponse] = Field(
        description="Comments",
        example=[
            _CommentInPostResponse(
                text="This is a comment", username="test", timestamp=datetime.now()
            ),
            _CommentInPostResponse(
                text="This is another comment",
                username="test2",
                timestamp=datetime.now(),
            ),
        ],
    )

    class Config:
        orm_mode = True

    class Config:
        orm_mode = True


class PostListResponse(BaseModel):
    posts: List[PostResponse] = Field(
        description="Posts",
        example=[
            PostResponse(
                id=1,
                image_url="https://example.com/img.jpg",
                caption="This is a caption",
                timestamp=datetime.now(),
                creator=_UserInPostResponse(username="test"),
                comments=[],
            ),
            PostResponse(
                id=2,
                image_url="https://example.com/img2.jpg",
                caption="This is a caption",
                timestamp=datetime.now(),
                creator=_UserInPostResponse(username="test2"),
                comments=[],
            ),
        ],
    )
