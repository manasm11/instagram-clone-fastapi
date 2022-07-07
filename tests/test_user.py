import os
import shutil
from unittest import TestCase

from fastapi import status
from fastapi.testclient import TestClient

from db import database, db_user
from main import app

client = TestClient(app)


class TestUserCreate(TestCase):

    original_db_file = database.SQLALCHEMY_DATABASE_URL.split("///")[1]

    def setUp(self):
        shutil.copy(self.original_db_file, "./db.backup")

    def tearDown(self):
        os.rename("./db.backup", self.original_db_file)

    def test_create_user(self):
        response = client.post("/user/", json={"username": "test", "password": "test"})
        json_response = response.json()

        assert response.status_code == status.HTTP_201_CREATED
        assert "username" in json_response
        assert "password" not in json_response
        assert json_response["username"] == "test"
