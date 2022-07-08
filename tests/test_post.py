from urllib import response

from tests.common import TestCase


class TestCreatePost(TestCase):
    def test_create_post(self):
        response = self.client.post(
            "/post/",
            json={
                "image_url": "https://example.com/image.jpg",
                "image_url_type": "absolute",
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

    def test_create_post__image_url__type_missing(self):
        response = self.create_post(image_url_type=None)
        self.check_error(response, "Image URL Type missing")

    def test_create_post__caption__missing(self):
        response = self.create_post(caption=None)
        self.check_error(response, "Caption missing")

    def test_create_post__creator_id__missing(self):
        response = self.create_post(creator_id=None)
        self.check_error(response, "Creator missing")

    def test_create_post__image_url__incorrect_format(self):
        response = self.create_post(image_url="Some Wrong Image URL")
        self.check_error(response, "Image URL is not valid")

    def test_create_post__image_url_type__incorrect(self):
        response = self.create_post(image_url_type="wrong")
        self.check_error(response, "Image URL Type must be 'absolute' or 'relative'")

    def test_create_post__creator_id__doesnt_exists(self):
        response = self.create_post(creator_id=int("9" * 12))
        self.check_error(response, "Creator (User) does not exist")

    def test_create_post__creator_id__incorrect_datatype(self):
        response = self.create_post(creator_id="a")
        self.check_error(response, "Creator Id incorrect")
