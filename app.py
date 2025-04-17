from flask import Flask, render_template, request, redirect, url_for
from PIL import Image
import pytesseract
import os

app = Flask(__name__)

# IMPORTANT: Ensure Tesseract is in your system's PATH or adjust if needed during deployment.
# DO NOT set pytesseract.pytesseract.tesseract_cmd here for Render deployment.
# Let pytesseract find tesseract in the PATH on the server.

def perform_ocr(image_path):
    """Performs OCR on the image and returns the extracted text."""
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.strip()  # Remove leading/trailing whitespace
    except Exception as e:
        return f"Error during OCR: {e}"

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
            # Save the uploaded image temporarily (in memory for simplicity, but consider saving to disk for larger files)
            image_path = "temp_image.png"  # Temporary filename
            image_file.save(image_path)  # Save to disk
            extracted_text = perform_ocr(image_path)
            os.remove(image_path) # Clean up the temporary image file

    return render_template('index.html', extracted_text=extracted_text)

if __name__ == '__main__':
    app.run(debug=True) # Run in debug mode for local development only