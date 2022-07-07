import re
import string
from time import time
from typing import Any

from pydantic import BaseModel, Field, ValidationError, validator


class UserRequest(BaseModel):
    username: Any = Field(
        ...,
        example=f"test_user_{int(time())%1000}",
        # max_length=20,
        # min_length=3,
        # regex="^[a-z0-9_]+$",
        description="Username must be lowercase alphanumeric of length 3-20",
    )
    password: str = Field(
        ...,
        example="Testing@321",
        max_length=20,
        min_length=8,
        regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{8,20}$",
        description="Password must be of length 8-20, contain at least one small alphabetical character, one capital alphabetical character, one numeric character, one numeric character, and one special character (@$!%*#?&)",
    )

    @validator("username")
    def username_must_be_string(cls, v):
        if v is None:
            raise ValueError("Missing username")
        return v

    @validator("username")
    def username_must_not_contain_special_characters(cls, v):
        invalid_chars = set(v).intersection(set(string.punctuation.replace("_", "")))
        chars = ", ".join(invalid_chars)
        if invalid_chars:
            raise ValueError(f"Username special characters not allowed: {chars}")
        return v

    @validator("username")
    def username_must_be_at_least_3_characters_long(cls, v):
        if len(v) < 3:
            raise ValueError("Username must be at least 3 characters long")
        return v

    @validator("username")
    def username_must_be_at_most_20_characters_long(cls, v):
        if len(v) > 20:
            raise ValueError("Username must be at most 20 characters long")
        return v

    @validator("username")
    def username_must_start_with_letter(cls, v):
        if not v[0].isalpha():
            raise ValueError("Username must start with a letter")
        return v

    @validator("username")
    def username_must_be_lower_case(cls, v):
        if v != v.lower():
            raise ValueError("Username must be lowercase")
        return v

    @validator("username")
    def username_must_not_contain_whitespace(cls, v):
        if re.search(r"\s", v):
            raise ValueError("Username cannot have whitespace")
        return v

    @validator("password")
    def password_must_be_string(cls, v):
        if v is None:
            raise ValueError("Missing password")
        return v


class UserResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True
