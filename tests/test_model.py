"""Tests for the preprocessing and prediction functions in model.py."""
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pytest

from model import predict_result, preprocess_img
from tests.conftest import make_image_bytes

SAMPLE_FIVE = Path(__file__).parent.parent / "test_images" / "5" / "Sign 5 (39).jpeg"


def test_preprocess_shape_and_range():
    """A real sample becomes a (1, 224, 224, 3) array with values in [0, 1]."""
    result = preprocess_img(str(SAMPLE_FIVE))
    assert result.shape == (1, 224, 224, 3)
    assert result.min() >= 0.0
    assert result.max() <= 1.0


def test_preprocess_accepts_stream():
    """Flask passes a file stream, not a path, so streams must work too."""
    result = preprocess_img(make_image_bytes(size=(500, 300)))
    assert result.shape == (1, 224, 224, 3)


@pytest.mark.parametrize("mode", ["RGBA", "L"])
def test_preprocess_non_rgb_images(mode):
    """PNG with transparency or grayscale images are converted to 3 channels."""
    result = preprocess_img(make_image_bytes(mode=mode))
    assert result.shape == (1, 224, 224, 3)


def test_preprocess_missing_file():
    """A path that does not exist raises FileNotFoundError."""
    with pytest.raises(FileNotFoundError):
        preprocess_img("does/not/exist.jpeg")


def test_predict_result_returns_argmax():
    """predict_result returns the index of the highest score (model is mocked)."""
    fake_scores = np.array([[0.05, 0.1, 0.05, 0.6, 0.2]])
    with patch("model.model.predict", return_value=fake_scores):
        assert predict_result(np.zeros((1, 224, 224, 3))) == 3
