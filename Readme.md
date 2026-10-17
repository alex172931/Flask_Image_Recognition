# Hand Digit Image Recognition

![CI](https://github.com/alex172931/Flask_Image_Recognition/actions/workflows/ci.yml/badge.svg)

This web app is made using Flask framework and is all about predicting the hand sign digit images based on the deep learning model trained using transfer learning.

![Python](https://img.shields.io/badge/python-8338ec)
![Keras](https://img.shields.io/badge/keras-219ebc)
![Numpy](https://img.shields.io/badge/numpy-ffafcc)
![Pillow](https://img.shields.io/badge/pillow-00bbf9)
![Flask](https://img.shields.io/badge/flask-f72585)
![Bootstrap](https://img.shields.io/badge/bootstrap-57cc99)

# Glimpse

https://user-images.githubusercontent.com/72191416/201943098-c8f5fd8b-ec7d-4e5d-883d-8b69109b946f.mp4

# Dependencies

- Flask
- TensorFlow (Keras)
- Numpy
- Pillow (PIL)

## UI Framework

- Bootstrap

# Get Started

Clone the repository in your project directory.

```commandline
git clone https://github.com/alex172931/Flask_Image_Recognition.git
```

# Install Dependencies

The project pins TensorFlow 2.10, which only supports **Python 3.10 or older**.
If your system has a newer Python, [uv](https://docs.astral.sh/uv/) can create a 3.10 environment for you:

```commandline
uv venv -p 3.10 .venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

# Run

```commandline
python app.py
```

Then open http://127.0.0.1:9000 in your browser.

# Test

- Choose an image from the test images folder.
- You will see a preview of the uploaded image.
- Click on **Submit** button and see the magic.

# Code Quality and Automated Tests

Install the development tools (Pylint, pre-commit) and enable the git hook:

```commandline
uv pip install -r requirements-dev.txt
pre-commit install
```

Run the checks locally:

```commandline
pylint $(git ls-files "*.py")
pytest -v
```

The same checks run on GitHub Actions on every push and pull request to `main` (see `.github/workflows/ci.yml`).
