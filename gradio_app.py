import base64
import cv2
import numpy as np
import gradio as gr

from server.util import classify_image, load_artifacts


def image_to_base64(image: np.ndarray) -> str:
    if image is None:
        raise ValueError("No image provided")

    success, buffer = cv2.imencode('.jpg', image)
    if not success:
        raise RuntimeError('Could not encode image')

    encoded = base64.b64encode(buffer).decode('utf-8')
    return f'data:image/jpeg;base64,{encoded}'


def classify_uploaded_image(image: np.ndarray):
    if image is None:
        return 'No image provided.', {}

    image_base64 = image_to_base64(image)
    results = classify_image(image_base64)
    if not results:
        return 'No face with two eyes found. Please upload a clearer photo.', {}

    prediction = results[0]
    probabilities = prediction['class_probability']
    if hasattr(probabilities, 'tolist'):
        probabilities = probabilities.tolist()
    if isinstance(probabilities, list) and probabilities and isinstance(probabilities[0], list):
        probabilities = probabilities[0]

    name_map = {value: key for key, value in prediction['class_dictionary'].items()}
    probabilities_dict = {
        name_map[index]: float(probabilities[index])
        for index in range(len(probabilities))
        if index in name_map
    }

    return prediction['class'], probabilities_dict


demo = gr.Interface(
    fn=classify_uploaded_image,
    inputs=gr.Image(type='numpy', label='Upload Image'),
    outputs=[
        gr.Textbox(label='Predicted Class'),
        gr.Label(num_top_classes=5, label='Class Probabilities')
    ],
    title='Face Image Classification',
    description='Upload an image containing a face. The model detects faces with at least two eyes and predicts the identity.',
    allow_flagging='never'
)

if __name__ == '__main__':
    load_artifacts()
    demo.launch()
