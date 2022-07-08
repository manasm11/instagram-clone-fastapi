import os
import shutil
import time
import unittest

from fastapi.testclient import TestClient
from requests import Response

from db import database
from main import app

RANDOM_STRING = (
    "!@#!@#!@#!@#!@#!@#!@!HDE(*EYD*&eyX(*&eyGX*(&(N ecn(* NH+18+-sefcr)&(*(*&^*("
)


class TestCase(unittest.TestCase):

    _ORIGINAL_DB_FILE = database.SQLALCHEMY_DATABASE_URL.split("///")[1]
    db = next(database.get_db())
    client = TestClient(app)

    def setUp(self):
        shutil.copy(self._ORIGINAL_DB_FILE, "./backup.db")
        self.create_user("manas", "Manas@123")

    def tearDown(self):
        os.rename("./backup.db", self._ORIGINAL_DB_FILE)

    def get_username(self):
        return f"test_user_{int(time.time())%1000}"

    def create_user(self, username=RANDOM_STRING, pwd="Testing@321"):
        if username == RANDOM_STRING:
            username = self.get_username()
        return self.client.post("/user/", json={"username": username, "password": pwd})

    def create_post(
        self,
        image_url="https://example.com/image.jpg",
        caption="My Khool caption is here.",
        creator_id=1,
    ):
        return self.client.post(
            "/post/",
            json={
                "image_url": image_url,
                "caption": caption,
                "creator_id": creator_id,
            },
        )

    def check_error(
        self,
        response: Response,
        message: str = None,
        status_code: int = 422,
        num_errors=1,
    ):
        response_json = response.json()
        self.assertEqual(response.status_code, status_code)
        self.assertIn("detail", response_json)
        self.assertIsInstance(response_json["detail"], list)
        self.assertEqual(len(response_json["detail"]), num_errors)
        if message:
            self.assertEqual(response_json["detail"][0]["msg"], message)
        return response_json["detail"][0]["msg"]
