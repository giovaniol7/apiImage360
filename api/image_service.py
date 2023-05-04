import cv2
from flask import Flask, Blueprint, request, jsonify

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"

@image.route('/stitch/<img>', methods=['POST'])
def stitch_images(img):
    # Recupera a lista de imagens enviada na requisição
    images = request.files.getlist(img)

    # Lê as imagens em memória usando OpenCV
    images_data = [cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR) for image in images]

    # Faz o stitch das imagens
    stitcher = cv2.createStitcher() if cv2.__version__.startswith('3') else cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch(images_data)

    # verifica se o stitching foi bem-sucedido
    if status != cv2.Stitcher_OK:
        print("Erro ao unir as imagens")
        return None

    # retorna a imagem resultante
    return stitched_image