import cv2
from flask import Flask, Blueprint, request, jsonify, Response, send_file
import numpy as np
import requests

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"  

def stitch_images(files):
    # cria um objeto Stitcher
    stitcher = cv2.createStitcher()

    # cria uma lista de imagens a serem unidas
    images = [cv2.imread(file) for file in files]

    # realiza o processo de stitching
    (status, result) = stitcher.stitch(images)

    # verifica se o stitching foi bem sucedido
    if status == cv2.Stitcher_OK:
        # retorna a imagem final
        return result
    else:
        # retorna uma mensagem de erro
        return 'Erro ao unir imagens: código de status {}'.format(status)

@image.route('/stitch', methods=['POST'])
def stitch():
    files = request.get_json()['files']
    result = stitch_files(files)
    if isinstance(result, str):
        return result
    else:
        # converte a imagem para o formato JPEG
        _, img_encoded = cv2.imencode('.jpg', result)
        response = Response(response=img_encoded.tobytes(), content_type='image/jpeg')
        return response