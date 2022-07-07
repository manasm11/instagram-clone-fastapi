import os
import shutil
import string
import time
from typing import List
from unittest import TestCase
from urllib import response

from fastapi import status
from fastapi.testclient import TestClient
from requests import Response

from db import database, db_user
from main import app

client = TestClient(app)


def create_user(username, password="Testing@321"):
    return client.post("/user/", json={"username": username, "password": password})


def get_unique_username():
    return f"test_user_{int(time.time())}"


def check_error(
    response: Response, message: str = None, status_code: int = 422, num_errors=1
):
    response_json = response.json()
    assert response.status_code == status_code
    assert "detail" in response_json
    assert isinstance(response_json.get("detail"), list)
    assert len(response_json["detail"]) == num_errors
    if message:
        assert response_json["detail"][0]["msg"] == message
    return response_json["detail"][0]["msg"]


class TestUserCreate(TestCase):

    original_db_file = database.SQLALCHEMY_DATABASE_URL.split("///")[1]

    def setUp(self):
        shutil.copy(self.original_db_file, "./backup.db")

    def tearDown(self):
        os.rename("./backup.db", self.original_db_file)

    # user create success
    def test_create_user(self):
        username = get_unique_username()
        response = client.post(
            "/user/", json={"username": username, "password": "Testing@123"}
        )
        json_response = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert "username" in json_response
        assert "password" not in json_response
        assert json_response["username"] == username

    def test_create_user__username_missing(self):
        response = create_user(None)
        check_error(response, "Missing username")

    def test_create_user__username_duplicate(self):
        username = get_unique_username()
        _response = create_user(username)
        assert _response.status_code == status.HTTP_201_CREATED

        check_error(
            create_user(username),
            f"User with username {username} already exists",
            status.HTTP_409_CONFLICT,
        )

    def test_create_user__username_special_chars(self):
        for character in string.punctuation.replace("_", ""):
            check_error(
                create_user("abc" + character),
                "Username special characters not allowed: " + character,
            )
        error_message = check_error(create_user("a#bf%l)*"))
        assert "Username special characters not allowed: " in error_message
        assert "#" in error_message
        assert "%" in error_message
        assert ")" in error_message
        assert "*" in error_message

    def test_create_user__username_start_with_number(self):
        check_error(create_user("1test"), "Username must start with a letter")

    def test_create_user__username_invalid_length(self):
        check_error(create_user(""), "Username must be at least 3 characters long")
        check_error(create_user("a"), "Username must be at least 3 characters long")
        check_error(
            create_user("a" * 21), "Username must be at most 20 characters long"
        )

    def test_create_user__username_must_be_lower_case(self):
        check_error(create_user("Test"), "Username must be lowercase")

    def test_create_user__username_has_whitespace(self):
        check_error(create_user("test test"), "Username cannot have whitespace")

    def test_create_user__username_with_multiple_errors(self):
        check_error(create_user("1he mTl"), num_errors=2)

    def test_create_user__password_invalid_length(self):
        assert False, "Not implemented"

    def test_create_user__password_missing(self):
        assert False, "Not implemented"

    def test_create_user__password_no_digit(self):
        assert False, "Not implemented"

    def test_create_user__password_no_upper_case(self):
        assert False, "Not implemented"

    def test_create_user__password_no_lower_case(self):
        assert False, "Not implemented"

    def test_create_user__password_no_special_char(self):
        assert False, "Not implemented"
