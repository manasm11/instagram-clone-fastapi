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


class UserNotExists(Exception):
    def __init__(self, username_or_id):
        if isinstance(username_or_id, int):
            self.message = f"User with id '{username_or_id}' doesn't exists"
        else:
            self.message = f"User with username '{username_or_id}' doesn't exists"


def user_not_exists(request: Request, exc: UserNotExists):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "user_not_exists"}]},
        status_code=status.HTTP_404_NOT_FOUND,
    )


class MultipleUsersWithSameUsername(Exception):
    def __init__(self, username: str, number_of_users: int):
        self.message = (
            f"Multiple ({number_of_users}) users with username '{username}' exists"
        )


def multiple_users_with_same_username(
    request: Request, exc: MultipleUsersWithSameUsername
):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "multiple_users_with_same_username"}]},
        status_code=status.HTTP_409_CONFLICT,
    )


class IncorrectPassword(Exception):
    def __init__(self):
        self.message = "Incorrect password"


def incorrect_password(request: Request, exc: IncorrectPassword):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "incorrect_password"}]},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


class PostNotExists(Exception):
    def __init__(self, post_id):
        self.message = f"Post with id '{post_id}' doesn't exists"


def post_not_exists(request: Request, exc: PostNotExists):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "post_not_exists"}]},
        status_code=status.HTTP_404_NOT_FOUND,
    )


class NotAuthorized(Exception):
    def __init__(self, message):
        self.message = " ".join(["You are not authorized", message])


def not_authorized(request: Request, exc: NotAuthorized):
    return JSONResponse(
        {"detail": [{"msg": exc.message, "type": "not_authorized"}]},
        status_code=status.HTTP_401_UNAUTHORIZED,
    )
