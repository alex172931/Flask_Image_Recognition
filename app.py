"""Flask web app that predicts the digit shown in a hand sign image."""
from flask import Flask, render_template, request

from model import preprocess_img, predict_result

app = Flask(__name__)


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
    except (KeyError, OSError, ValueError):
        # KeyError: no "file" field in the form
        # OSError: empty upload or file that Pillow cannot read as an image
        # ValueError: image data with an unexpected shape
        error = "File cannot be processed."
        return render_template("result.html", err=error)


if __name__ == "__main__":
    app.run(port=9000, debug=True)
