"""Flask web app that predicts the digit shown in a hand sign image."""
import os
import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect
from PIL import Image

from model import preprocess_img, predict_result

# Biggest upload the app accepts (5 MB); bigger requests get HTTP 413
MAX_UPLOAD_BYTES = 5 * 1024 * 1024

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = MAX_UPLOAD_BYTES
# Key used to sign the CSRF tokens. Set SECRET_KEY on a real server;
# without it, a random key is created when the app starts.
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY") or secrets.token_hex(32)
# Every POST form must send a valid csrf_token, otherwise Flask returns 400
csrf = CSRFProtect(app)


@app.route("/")
def main():
    """Show the upload page."""
    return render_template("index.html")


@app.route("/prediction", methods=["POST"])
def predict_image_file():
    """Preprocess the uploaded image, run the model and show the predicted digit."""
    try:
        img = preprocess_img(request.files["file"].stream)
        pred = predict_result(img)
        return render_template("result.html", predictions=str(pred))
    except (KeyError, OSError, ValueError, Image.DecompressionBombError):
        # KeyError: no "file" field in the form
        # OSError: empty upload or file that Pillow cannot read as an image
        # ValueError: image data with an unexpected shape
        # DecompressionBombError: image with far too many pixels (memory attack)
        error = "File cannot be processed."
        return render_template("result.html", err=error)


@app.errorhandler(413)
def file_too_large(_error):
    """Show the error page when the upload is bigger than MAX_UPLOAD_BYTES."""
    return render_template("result.html", err="File is too large (max 5 MB)."), 413


if __name__ == "__main__":
    # Debug mode only when FLASK_DEBUG=1 is set, never by default
    app.run(port=9000, debug=os.environ.get("FLASK_DEBUG") == "1")
