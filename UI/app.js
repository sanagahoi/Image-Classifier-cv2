const imageInput = document.getElementById('imageInput');
const previewImage = document.getElementById('previewImage');
const previewHint = document.getElementById('previewHint');
const classifyBtn = document.getElementById('classifyBtn');
const statusMessage = document.getElementById('statusMessage');
const resultDetails = document.getElementById('resultDetails');

let selectedImageBase64 ='';

imageInput.addEventListener('change', async (event) => {
    const file = event.target.files[0];
    if (!file) {
        resetPreview();
        return;
    }

    const reader = new FileReader();
    reader.onload = () => {
        selectedImageBase64 = reader.result;
        previewImage.src = selectedImageBase64;
        previewImage.style.display = 'block';
        previewHint.textContent = 'Preview of the selected image.';
        classifyBtn.disabled = false;
        statusMessage.textContent = 'Ready to classify the selected image.';
        statusMessage.className = 'status';
        resultDetails.innerHTML = '';
    };
    reader.readAsDataURL(file);
});

classifyBtn.addEventListener('click', async () => {
    if (!selectedImageBase64) {
        return;
    }

    setStatus('Classifying image...', '');
    classifyBtn.disabled=true;

    try {
        const response = await fetch('http://127.0.0.1:5000/classify_image', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({
                image_data: selectedImageBase64,
            }),
        });

        if (!response.ok) {
            throw new Error(`Server returned status ${response.status}`);
        }

        const data = await response.json();
        renderResult(data);
    } catch (error) {
        setStatus(`Failed to classify image: ${error.message}`, 'error');
        resultDetails.innerHTML = '';
    } finally {
        classifyBtn.disabled = false;
    }
});

function setStatus(message, type = '') {
    statusMessage.textContent = message;
    statusMessage.className = type ? `status ${type}` : 'status';
}

function resetPreview() {
    previewImage.src = '';
    previewImage.style.display = 'none';
    previewHint.textContent = 'Choose an image to preview here.';
    classifyBtn.disabled = true;
    setStatus('No image selected.', '');
    resultDetails.innerHTML = '';
}

function formatProbability(probArray) {
    if (!Array.isArray(probArray)) {
        return '';
    }
    const values = Array.isArray(probArray[0]) ? probArray[0] : probArray;
    return values
        .map((value, index) => `<div>${index + 1}. ${Number(value).toFixed(4)}</div>`)
        .join('');
}

function renderResult(data) {
    if (!Array.isArray(data) || data.length === 0) {
        setStatus('No faces detected or classification returned no results.', 'error');
        resultDetails.innerHTML = '';
        return;
    }

    setStatus('Classification complete.', 'success');
    resultDetails.innerHTML = '';

    data.forEach((item, index) => {
        const probabilityText = item.class_probability ? formatProbability(item.class_probability) : 'Unknown';
        const dictionaryText = item.class_dictionary
            ? Object.entries(item.class_dictionary)
                  .map(([label, id]) => `${label}: ${id}`)
                  .join('<br>')
            : 'Unavailable';

        const card = document.createElement('div');
        card.className = 'detail-item';
        card.innerHTML = `
            <strong>Face ${index + 1}</strong>
            <span><strong>Predicted class:</strong> ${item.class || 'Unknown'}</span>
            <span><strong>Class probabilities:</strong><br>${probabilityText}</span>
            <span><strong>Class dictionary:</strong><br>${dictionaryText}</span>
        `;

        resultDetails.appendChild(card);
    });
}

resetPreview();
