"""Shared pytest fixtures for the Flask app and generated test images."""
import io

import pytest
from PIL import Image

from app import app as flask_app


@pytest.fixture(name="client")
def fixture_client():
    """Flask test client, so requests run without starting a real server."""
    flask_app.config["TESTING"] = True
    with flask_app.test_client() as test_client:
        yield test_client


def make_image_bytes(mode="RGB", size=(64, 64), fmt="PNG"):
    """Build a small in-memory image and return it as a BytesIO object."""
    buffer = io.BytesIO()
    Image.new(mode, size).save(buffer, format=fmt)
    buffer.seek(0)
    return buffer
