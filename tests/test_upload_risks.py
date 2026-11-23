"""Tests for upload risks that SonarQube Cloud did not report."""
import io

from PIL import Image

from tests.conftest import make_image_bytes

ERROR_MESSAGE = b"File cannot be processed."


def post_file(client, data):
    """Send a multipart POST request to the prediction route."""
    return client.post("/prediction", data=data, content_type="multipart/form-data")


def test_decompression_bomb_shows_error(client, monkeypatch):
    """An image with too many pixels shows the error page instead of crashing (HTTP 500)."""
    # Lower the Pillow limit so a small test image is treated like a huge one
    monkeypatch.setattr(Image, "MAX_IMAGE_PIXELS", 1000)
    response = post_file(client, {"file": (make_image_bytes(size=(64, 64)), "bomb.png")})
    assert response.status_code == 200
    assert ERROR_MESSAGE in response.data


def test_upload_bigger_than_limit_is_rejected(client):
    """A request body bigger than 5 MB is refused with HTTP 413."""
    big_file = io.BytesIO(b"0" * (5 * 1024 * 1024 + 1))
    response = post_file(client, {"file": (big_file, "big.png")})
    assert response.status_code == 413
    assert b"File is too large" in response.data
