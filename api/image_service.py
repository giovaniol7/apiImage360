import cv2
from flask import Flask, Blueprint, request, jsonify, Response, send_file
import numpy as np
import requests
import os

image = Blueprint('image',__name__)

app.config['IMAGES_FOLDER'] = 'caminho/para/a/pasta/de/imagens'

@image.route('/')
def instructions():
    return "Image"  

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@image.route('/upload', methods=['POST'])
def upload():
    # montar o caminho completo para o arquivo de imagem
    filepath = os.path.join(app.config['IMAGES_FOLDER'], filename)
    # verificar se o arquivo de imagem existe
    if not os.path.isfile(filepath):
        return Response(status=404)
    # retornar a imagem como uma resposta com o tipo de mídia correto
    return send_file(filepath, mimetype='image/jpeg')

def stitch_images(files):
    stitcher = cv2.createStitcher()
    images = [cv2.imread(file) for file in files]
    (status, result) = stitcher.stitch(images)
    if status == cv2.Stitcher_OK:
        return result
    else:
        return 'Erro ao unir imagens: código de status {}'.format(status)

@image.route('/stitch/<imgList>', methods=['GET'])
def stitch():
    files = request.get_json()['imgList']
    result = stitch_files(files)
    if isinstance(result, str):
        return result
    else:
        # converte a imagem para o formato JPEG
        _, img_encoded = cv2.imencode('.jpg', result)
        response = Response(response=img_encoded.tobytes(), content_type='image/jpeg')
        return response