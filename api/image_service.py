import cv2
from flask import Flask, Blueprint, request, jsonify, Response, send_file, send_from_directory
import numpy as np
import requests
import os
from werkzeug.utils import secure_filename

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"  

@image.route('/upload', methods=['POST'])
def upload():
   if request.method=="POST":

        pasta = './stitchImage/'

        if os.path.exists(pasta):
            for arquivo in os.listdir(pasta):
                if arquivo.endswith('.jpg'):
                    os.remove(os.path.join(pasta, arquivo))

        pasta2 = './upload/'

        if not os.path.exists(pasta2):
            os.makedirs(pasta2)

        #taking image from flutter front-end 
        imagefile=request.files['imagem']
        filename=secure_filename(imagefile.filename)
        #saving image temporarily in "upload" folder 
        imagefile.save("./upload/"+filename)
        img="./upload/"+filename
        return filename

@image.route('/stitch')
def get_stitched_image():
    # Call stitch_images() to stitch the images and save the stitched image
    stitch_images()

    stitched_image_path = 'stitchImage/stitched_image.jpg'

    pasta = './upload/'
    pasta2 = './stitchImage/'

    # Check if stitched image exists
    if not os.path.exists(pasta2):
        for arquivo in os.listdir(pasta2):
            if arquivo.endswith('.jpg'):
                return jsonify({'message': 'Image success.'}), 200
        return jsonify({'error': 'Stitched image not found.'}), 404

    for arquivo in os.listdir(pasta):
        if arquivo.endswith('.jpg'):
            os.remove(os.path.join(pasta, arquivo))

    # Return the stitched image
    return send_file(stitched_image_path, mimetype='image/jpg')

def stitch_images():
    upload_dir = 'upload'
    image_paths = [os.path.join(upload_dir, f) for f in os.listdir(upload_dir) if f.endswith('.jpg')]

    images = []
    for path in image_paths:
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        images.append(img)

    stitcher = cv2.createStitcher() #if cv2.__version__.startswith('3') else cv2.Stitcher.create()
    status, stitched_image = stitcher.stitch(images)
    if status != cv2.Stitcher_OK:
        return jsonify({'error': 'Image stitching failed.'}), 500
    else:
        # Save stitched image to output directory
        output_dir = 'stitchImage'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, 'stitched_image.jpg')
        cv2.imwrite(output_path, stitched_image)

        return jsonify({'message': 'Image success.'}), 200