from pydantic import BaseModel


class UserRequest(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str

    class Config:
        orm_mode = True
