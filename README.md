# Image Classifier with OpenCV

This project is a beginner-friendly computer vision application that classifies face images into known categories using OpenCV, image processing techniques, and a pre-trained machine learning model. It is designed as a simple demonstration of how image classification can be built from scratch with Python.

## What the project does

The application allows users to upload an image and predicts the identity of the person in the image when a face with two visible eyes is detected. It combines:

- OpenCV-based face and eye detection
- Wavelet feature extraction
- A trained scikit-learn classifier
- A simple web interface for easy interaction

## Features

- Upload an image through a web interface
- Detect faces and verify that the image contains a face with two eyes
- Predict the most likely class for the detected face
- Display class probabilities for the available labels
- Provide a lightweight Flask API for image classification

## Project structure

- app.py: Gradio-based web application
- gradio_app.py: Alternative Gradio interface
- server/server.py: Flask API for classifying uploaded images
- server/util.py: Image preprocessing and prediction logic
- server/artifacts/: Pre-trained model and class mapping files
- opencv/: Haar cascade files used for face and eye detection

## Requirements

Make sure you have Python 3.9 or newer installed.

Install the required dependencies:

```bash
pip install -r requirements.txt
```

## Getting started

1. Clone the repository.
2. Install the dependencies.
3. Run the application.

### Option 1: Run the Gradio app

```bash
python app.py
```

### Option 2: Run the Flask API

```bash
cd server
python server.py
```

## Usage tips

- Use a clear, front-facing image for better results.
- The model performs best when the face is visible and the eyes are detectable.
- If the image does not contain a suitable face, the app will return a message asking for a clearer photo.

## Notes

This project is intended for learning and demonstration purposes. It is not a production-grade facial recognition system and should be used carefully and responsibly.
