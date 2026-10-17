"""Loading of the Keras model and helpers to preprocess images and predict digits."""
from pathlib import Path

import numpy as np
from keras.models import load_model
from keras.utils import img_to_array
from PIL import Image

MODEL_PATH = Path(__file__).parent / "digit_model.h5"
IMAGE_SIZE = (224, 224)

# Loaded once when the module is imported, then reused for every request
model = load_model(MODEL_PATH)


def preprocess_img(image_source):
    """Open an image (path or file stream) and return a (1, 224, 224, 3) array in [0, 1]."""
    op_img = Image.open(image_source)
    img_resize = op_img.resize(IMAGE_SIZE)
    img2arr = img_to_array(img_resize) / 255.0
    img_reshape = img2arr.reshape(1, IMAGE_SIZE[0], IMAGE_SIZE[1], 3)
    return img_reshape


def predict_result(img_array):
    """Run the model on a preprocessed image and return the predicted digit."""
    pred = model.predict(img_array)
    return np.argmax(pred[0], axis=-1)
