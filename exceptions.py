from fastapi import Request, status
from fastapi.responses import JSONResponse


class UserExists(Exception):
    def __init__(self, username):
        self.message = f"User with username '{username}' already exists"


def user_exists(request: Request, exc: UserExists):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "user_exists"}]},
        status_code=status.HTTP_409_CONFLICT,
    )


class InvalidImageExtension(Exception):
    def __init__(self, filename):
        self.message = f"Image file '{filename}' has invalid extension"


def invalid_image_extension(request: Request, exc: InvalidImageExtension):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "invalid_image_extension"}]},
        status_code=status.HTTP_400_BAD_REQUEST,
    )
