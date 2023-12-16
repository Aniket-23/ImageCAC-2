from flask import Flask, render_template, request, redirect, url_for
import cv2
import os
import numpy as np
from werkzeug.utils import secure_filename

app = Flask(__name__)

# Set the upload folder inside the static folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Ensure the upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def apply_canny_edge_detection(image_path):
    # Read the image
    image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    # Apply Canny edge detection
    edges = cv2.Canny(image, 0, 50)

    # Save the processed image in the static/uploads folder
    edge_image_path = os.path.join(app.config['UPLOAD_FOLDER'], 'edge_' + secure_filename(image_path))
    cv2.imwrite(edge_image_path, edges)

    return edge_image_path

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadImage', methods=['GET', 'POST'])
def upload_image():
    original_image = None
    edge_image = None

    if request.method == 'POST':
        # Check if the post request has the file part
        if 'imageFile' not in request.files:
            return redirect(request.url)

        file = request.files['imageFile']

        # If the user does not select a file, the browser submits an empty file without a filename
        if file.filename == '':
            return redirect(request.url)

        # Check if the file is allowed
        if file and file.filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
            # Save the uploaded file in the static/uploads folder
            filename = secure_filename(file.filename)
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(image_path)

            # Apply Canny edge detection
            edge_image_path = apply_canny_edge_detection(image_path)

            # Set paths to pass to the template
            original_image = 'static/uploads/' + filename
            edge_image = 'static/uploads/edge_static_uploads_' + filename
            
    # Render the template with image paths
    return render_template('uploadImage.html', original_image=original_image, edge_image=edge_image)


if __name__ == '__main__':
    app.run(debug=True)
