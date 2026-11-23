"""Tests for the CSRF protection added with Flask-WTF."""
import re
from unittest.mock import patch

import pytest

from app import app as flask_app
from tests.conftest import make_image_bytes

TOKEN_PATTERN = re.compile(r'name="csrf_token" type="hidden" value="([^"]+)"')


@pytest.fixture(name="csrf_client")
def fixture_csrf_client():
    """Test client with CSRF protection turned on, like on a real server."""
    flask_app.config["TESTING"] = True
    flask_app.config["WTF_CSRF_ENABLED"] = True
    with flask_app.test_client() as test_client:
        yield test_client
    flask_app.config["WTF_CSRF_ENABLED"] = False


def test_form_contains_csrf_token(csrf_client):
    """The upload page puts a hidden csrf_token field in the form."""
    page = csrf_client.get("/").get_data(as_text=True)
    assert TOKEN_PATTERN.search(page) is not None


def test_post_without_token_is_refused(csrf_client):
    """A POST that does not come from our form (no token) gets HTTP 400."""
    with patch("app.predict_result") as mocked_predict:
        response = csrf_client.post(
            "/prediction",
            data={"file": (make_image_bytes(), "hand.png")},
            content_type="multipart/form-data",
        )
    assert response.status_code == 400
    mocked_predict.assert_not_called()


def test_post_with_token_works(csrf_client):
    """A POST with the token from the page is accepted and shows the prediction."""
    page = csrf_client.get("/").get_data(as_text=True)
    token = TOKEN_PATTERN.search(page).group(1)
    with patch("app.predict_result", return_value=4):
        response = csrf_client.post(
            "/prediction",
            data={"csrf_token": token, "file": (make_image_bytes(), "hand.png")},
            content_type="multipart/form-data",
        )
    assert response.status_code == 200
    assert b">4</h2>" in response.data
