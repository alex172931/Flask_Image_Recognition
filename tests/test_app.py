"""Tests for the Flask routes in app.py."""
import io
from pathlib import Path
from unittest.mock import patch

from tests.conftest import make_image_bytes

SAMPLE_FIVE = Path(__file__).parent.parent / "test_images" / "5" / "Sign 5 (39).jpeg"
ERROR_MESSAGE = b"File cannot be processed."


def post_file(client, data):
    """Send a multipart POST request to the prediction route."""
    return client.post("/prediction", data=data, content_type="multipart/form-data")


def test_home_page_loads(client):
    """GET / returns the upload page."""
    response = client.get("/")
    assert response.status_code == 200
    assert b"Hand Sign Digit Language Detection" in response.data
    assert b'name="file"' in response.data


def test_prediction_with_mocked_model(client):
    """A valid image shows the value returned by the model (model is mocked)."""
    with patch("app.predict_result", return_value=7) as mocked_predict:
        response = post_file(client, {"file": (make_image_bytes(), "hand.png")})
    assert response.status_code == 200
    assert b">7</h2>" in response.data
    mocked_predict.assert_called_once()


def test_prediction_with_real_model(client):
    """End-to-end check with the real model on a known sample of the digit 5."""
    with open(SAMPLE_FIVE, "rb") as image_file:
        response = post_file(client, {"file": (image_file, SAMPLE_FIVE.name)})
    assert response.status_code == 200
    assert b">5</h2>" in response.data


def test_missing_file_field(client):
    """A POST without any file field shows the error message."""
    with patch("app.predict_result") as mocked_predict:
        response = post_file(client, {})
    assert ERROR_MESSAGE in response.data
    mocked_predict.assert_not_called()


def test_empty_file(client):
    """An empty upload (no file selected in the browser) shows the error message."""
    response = post_file(client, {"file": (io.BytesIO(b""), "")})
    assert ERROR_MESSAGE in response.data


def test_non_image_file(client):
    """A text file renamed as .jpg is rejected instead of crashing the app."""
    fake_image = io.BytesIO(b"this is not an image")
    response = post_file(client, {"file": (fake_image, "fake.jpg")})
    assert response.status_code == 200
    assert ERROR_MESSAGE in response.data


def test_get_on_prediction_not_allowed(client):
    """The prediction route only accepts POST."""
    response = client.get("/prediction")
    assert response.status_code == 405
