from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import os
import requests  # Import the requests library

app = Flask(__name__)

# OCR Space API Configuration
OCR_SPACE_API_URL = "https://api.ocr.space/parse/image"
OCR_SPACE_API_KEY = "K87955728688957"  #  <--- REPLACE WITH YOUR ACTUAL API KEY!

def perform_ocr(image_path):
    """Performs OCR using OCR Space API and returns extracted text."""
    try:
        with open(image_path, 'rb') as f:
            image_data = f.read()

        payload = {
            'apikey': OCR_SPACE_API_KEY,
            'language': 'eng'  # You can change language if needed (e.g., 'deu' for German)
        }
        files = {'image': ('image.png', image_data)} # Filename doesn't matter much for OCR Space

        response = requests.post(OCR_SPACE_API_URL, files=files, data=payload)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)

        result = response.json()

        if result and result.get('IsErroredOnProcessing') == False:
            text = result.get('ParsedResults')[0].get('ParsedText') if result.get('ParsedResults') else "No text found in image."
            return text.strip()
        else:
            error_message = result.get('ErrorMessage') or "Unknown error from OCR Space API."
            return f"OCR Space API Error: {error_message}"

    except requests.exceptions.RequestException as e:
        return f"Error connecting to OCR Space API: {e}"
    except Exception as e:
        return f"Error during OCR processing: {e}"


@app.route('/', methods=['GET', 'POST'])
def index():
    extracted_text = None
    if request.method == 'POST':
        if 'image' not in request.files:
            return "No image part"

        image_file = request.files['image']

        if image_file.filename == '':
            return "No selected image"

        if image_file:
            image_path = "temp_image.png"
            image_file.save(image_path)
            extracted_text = perform_ocr(image_path)
            os.remove(image_path)

    return render_template('index.html', extracted_text=extracted_text)


if __name__ == '__main__':
    app.run(debug=True)