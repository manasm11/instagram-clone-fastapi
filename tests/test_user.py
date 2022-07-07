import os
import shutil
import time
from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient

from db import database, db_user
from main import app

client = TestClient(app)


def create_user(username, password):
    return client.post("/user/", json={"username": username, "password": password})


def get_unique_username():
    return f"test_user_{time.time()}"


class TestUserCreate(TestCase):

    original_db_file = database.SQLALCHEMY_DATABASE_URL.split("///")[1]

    def setUp(self):
        shutil.copy(self.original_db_file, "./backup.db")

    def tearDown(self):
        os.rename("./backup.db", self.original_db_file)

    def test_create_user(self):
        username = get_unique_username()
        response = client.post(
            "/user/", json={"username": username, "password": "test"}
        )
        json_response = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert "username" in json_response
        assert "password" not in json_response
        assert json_response["username"] == username

    def test_create_user_with_existing_username(self):
        username = get_unique_username()
        _response = create_user(username, "test")
        assert _response.status_code == status.HTTP_201_CREATED

        response = create_user(username, "test")
        json_response = response.json()
        assert response.status_code == status.HTTP_409_CONFLICT
        assert "detail" in json_response
        assert (
            json_response["detail"] == f"User with username {username} already exists"
        )
