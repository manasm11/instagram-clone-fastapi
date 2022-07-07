from fastapi import Request, status
from fastapi.responses import JSONResponse


class UserExists(Exception):
    def __init__(self, username):
        self.message = f"User with username {username} already exists"


def user_exists(request: Request, exc: UserExists):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "user_exists"}]},
        status_code=status.HTTP_409_CONFLICT,
    )
