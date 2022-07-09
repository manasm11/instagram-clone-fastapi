from urllib import response

from tests.common import TestCase


class TestCreatePost(TestCase):
    def test_create_post(self):
        response = self.client.post(
            "/post/",
            json={
                "image_url": "https://example.com/image.jpg",
                "caption": "This is a caption",
                "creator_id": 1,
            },
        )
        assert response.status_code == 201, "Response code is not 201"
        response_json = response.json()
        assert response_json["image_url"] == "https://example.com/image.jpg"
        assert response_json["image_url_type"] == "absolute"
        assert response_json["caption"] == "This is a caption"
        assert "id" in response_json
        assert "timestamp" in response_json
        assert "creator" in response_json

    def test_create_post__image_url__missing(self):
        response = self.create_post(image_url=None)
        self.check_error(response, "Image URL missing")

    def test_create_post__caption__missing(self):
        response = self.create_post(caption=None)
        self.check_error(response, "Caption missing")

    def test_create_post__creator_id__missing(self):
        response = self.create_post(creator_id=None)
        self.check_error(response, "Creator missing")

    def test_create_post__image_url__accepts_relative_urls(self):
        response = self.create_post(image_url="/image.jpg")
        assert (
            response.status_code == 201
        ), f"Response code is not 201, {response.json()}"
        response_json = response.json()
        assert response_json["image_url"] == "/image.jpg"
        assert response_json["image_url_type"] == "relative"

    def test_create_post__image_url__incorrect_format(self):
        msg = "Image URL is not valid: '{}'"
        self.check_error(self.create_post(image_url="wrong"), msg.format("wrong"))
        self.check_error(
            self.create_post(image_url="http:/localhost:8000/abcd.gif"),
            msg.format("http:/localhost:8000/abcd.gif"),
        )

    def test_create_post__creator_id__doesnt_exists(self):
        response = self.create_post(creator_id=int("9" * 12))
        self.check_error(response, "Creator (User) does not exist")

    def test_create_post__creator_id__incorrect_datatype(self):
        response = self.create_post(creator_id="a")
        self.check_error(response, "Creator Id incorrect")

    def test_create_post__requires_authentication(self):
        assert False, "Not implemented"


class TestGetAllPost(TestCase):
    def test_get_all_post__success(self):
        self.create_post(caption="Some caption")
        response = self.client.get("/post/all/")
        assert response.status_code == 200
        response_json = response.json()
        assert "posts" in response_json
        assert isinstance(response_json["posts"], list)
        assert len(response_json["posts"]) == 1
        assert response_json["posts"][0]["caption"] == "Some caption"

    def test_get_all_post__timestamp_ordering(self):
        self.create_post(caption="First Post")
        self.create_post(caption="Second Post")
        response = self.client.get("/post/all/")
        response_json = response.json()
        assert len(response_json["posts"]) == 2
        assert response_json["posts"][0]["caption"] == "Second Post"
        assert response_json["posts"][1]["caption"] == "First Post"
