import os
import base64
import numpy as np
import cv2
import gradio as gr
from server.util import load_artifacts, classify_image


def image_to_base64(image):
    if image is None:
        return None

    if not isinstance(image, np.ndarray):
        image = np.array(image)

    if image.ndim == 2:
        image = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    elif image.shape[2] == 4:
        image = cv2.cvtColor(image, cv2.COLOR_RGBA2BGR)
    else:
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    success, encoded_image = cv2.imencode('.jpg', image)
    if not success:
        return None

    return 'data:image/jpeg;base64,' + base64.b64encode(encoded_image.tobytes()).decode('utf-8')


def format_results(results):
    if not results:
        return 'No face with two eyes detected.'

    lines = []
    for idx, item in enumerate(results, start=1):
        lines.append(f'Face {idx}: {item["class"]}')
        probs = item['class_probability'][0]
        lines.append('Probabilities:')
        for label, label_index in item['class_dictionary'].items():
            lines.append(f'  {label}: {probs[label_index]:.2%}')
        lines.append('')
    return '\n'.join(lines)


def predict(image):
    if image is None:
        return 'Upload an image to classify.'

    image_base64 = image_to_base64(image)
    if image_base64 is None:
        return 'Could not process image. Please try a different file.'

    results = classify_image(image_base64)
    return format_results(results)


if __name__ == '__main__':
    load_artifacts()

    demo = gr.Interface(
        fn=predict,
        inputs=gr.Image(type='numpy', label='Upload image'),
        outputs=gr.Textbox(label='Prediction'),
        title='Face Image Classification',
        description='Upload a face image and predict the person using the trained model.',
        allow_flagging='never'
    )

    port = int(os.environ.get('PORT', 8000))
    demo.launch(server_name='0.0.0.0', server_port=port, share=False)
