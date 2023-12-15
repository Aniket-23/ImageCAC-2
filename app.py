from flask import Flask, render_template, request, redirect, url_for
import cv2
import numpy as np
from matplotlib import pyplot as plt
import pydicom

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/uploadImage')
def upload_image():
    return render_template('uploadImage.html')

if __name__ == '__main__':
    app.run(debug=True)
