import cv2
from flask import Flask, Blueprint, request, jsonify, Response, send_file, send_from_directory
import numpy as np
import requests
import os
from werkzeug.utils import secure_filename
import imutils
from imutils import paths

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"  

@image.route('/upload', methods=['POST'])
def upload():
   if request.method=="POST":
    #   pasta = './stitchImage/'
        pastatemp = './temp/'
        if os.path.exists(pastatemp):
            for arquivo in os.listdir(pastatemp):
                os.remove(os.path.join(pastatemp, arquivo))
        #   if os.path.exists(pasta):
        #       for arquivo in os.listdir(pasta):
        #           if arquivo.endswith('.jpg'):
        #               os.remove(os.path.join(pasta, arquivo))
        #           if arquivo.endswith('.png'):
        #               os.remove(os.path.join(pasta, arquivo))
        #taking image from flutter front-end 
        
        imagefile=request.files['imagem']
        filename=secure_filename(imagefile.filename)
        #saving image temporarily in "upload" folder 
        #img="./upload/"+filename
        
        input_path = os.path.join("./upload/", filename)
        cv2.imwrite(input_path, imagefile)
        
        #imagefile.save("./upload/"+filename)
        
        return filename

@image.route('/stitch', methods=['GET'])
def get_stitched_image():
    # Call stitch_images() to stitch the images and save the stitched image
    stitch_images()

    stitched_image_path = 'stitchImage/stitched_image.png'

    pasta = './upload/'
    pasta2 = './stitchImage/'
    
    if not os.path.exists(stitched_image_path):
        return jsonify({'error': 'Stitched image not found.'}), 404

    for arquivo in os.listdir(pasta):
        os.remove(os.path.join(pasta, arquivo))
        

    return send_file(stitched_image_path, mimetype='image/png')


def stitch_images():
    upload_dir = './upload/'
    #temp_dir = './temp/'
    image_paths = [os.path.join(upload_dir, f) for f in os.listdir(upload_dir) if f.endswith(('.jpeg', '.png'))]

    images = []

    for i, path in enumerate(image_paths):
        img = cv2.imread(path)
        img = np.array(img)

        #if(len(img.shape)==2):
        #    img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)

        filename = f'./temp/image{i}.png'
        cv2.imwrite(filename, img)

        images.append(cv2.imread(filename))
        
    #for path in image_paths:
    #    img = cv2.imread(path)
    #    img = np.array(img)
    #    if(len(img.shape)==2):
    #        img = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
    #    images.append(img)

    stitcher = cv2.createStitcher() if cv2.__version__.startswith('3') else cv2.Stitcher.create()
    status, stitched_image = stitcher.stitch(images)
    print(status)
    if status != cv2.Stitcher_OK:
        return jsonify({'error': 'Image stitching failed.'}), 500
    else:
        stitched_image = cv2.copyMakeBorder(stitched_image, 10, 10, 10, 10, cv2.BORDER_CONSTANT, (0, 0, 0))
        gray = cv2.cvtColor(stitched_image, cv2.COLOR_BGR2GRAY)
        thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY)[1]

        cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)

        mask = np.zeros(thresh.shape, dtype="uint8")
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(mask, (x, y), (x + w, y + h), 255, -1)

        minRect = mask.copy()
        sub = mask.copy()
        while cv2.countNonZero(sub) > 0:
            minRect = cv2.erode(minRect, None)
            sub = cv2.subtract(minRect, thresh)
            
        cnts = cv2.findContours(minRect.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        cnts = imutils.grab_contours(cnts)
        c = max(cnts, key=cv2.contourArea)
        (x, y, w, h) = cv2.boundingRect(c)
        stitched_image = stitched_image[y:y + h, x:x + w]

        # Save stitched image to output directory    
        output_dir = './stitchImage/'
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        output_path = os.path.join(output_dir, 'stitched_image.png')
        cv2.imwrite(output_path, stitched_image)

        return jsonify({'message': 'Image success.'}), 200