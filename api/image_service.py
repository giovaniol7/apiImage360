import cv2
from flask import Flask, Blueprint, request, jsonify, Response, send_file
import numpy as np
import requests
import werkzeug

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"  

@image.route('/upload', methods=['POST'])
def upload():
    if(request.methods == "POST"):
        imagefile = request.file['imageFile']
        filename = werkzeug.utils.secure_filename(imagefile.filename)
        imagefile.save = ("./output/" + filename)
        return jsonify({
            "message": "Imagem uploud com sucesso"
        })