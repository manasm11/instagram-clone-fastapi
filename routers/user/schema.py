import re
import string
from time import time
from typing import Any

from pydantic import BaseModel, Field, ValidationError, validator


class UserRequest(BaseModel):
    username: Any = Field(
        ...,
        example=f"test_user_{int(time())%1000}",
        description="Username must be lowercase alphanumeric of length 3-20",
    )
    password: Any = Field(
        ...,
        example=f"Testing@{int(time()%1000)}",
        description="Password must be of length 8-20, contain at least one small alphabetical character, one capital alphabetical character, one numeric character, one numeric character, and one special character (@$!%*#?&)",
    )

    @validator("username")
    def username_must_be_string(cls, v):
        if v is None:
            raise ValueError("Username missing")
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        if len(v) > 20:
            raise ValueError("Username must be at most 20 characters long")
        invalid_chars = set(v).intersection(set(string.punctuation.replace("_", "")))
        chars = ", ".join(invalid_chars)
        if invalid_chars:
            raise ValueError(f"Username special characters not allowed: {chars}")
        if not v[0].isalpha():
            raise ValueError("Username must start with a letter")
        if v != v.lower():
            raise ValueError("Username must be lowercase")
        if re.search(r"\s", v):
            raise ValueError("Username cannot have whitespace")
        return v

    @validator("password")
    def password_must_be_string(cls, v):
        if v is None:
            raise ValueError("Password missing")
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters long")
        if len(v) > 20:
            raise ValueError("Password must be at most 20 characters long")
        if not set(string.ascii_lowercase).intersection(set(v)):
            raise ValueError("Password must contain lowercase letter")
        if not set(string.ascii_uppercase).intersection(set(v)):
            raise ValueError("Password must contain uppercase letter")
        if not set(string.punctuation).intersection(set(v)):
            raise ValueError("Password must contain special character")
        if not set(string.digits).intersection(set(v)):
            raise ValueError("Password must contain digits")
        return v


class UserResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True
