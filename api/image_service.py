import cv2
from flask import Flask, Blueprint, request, jsonify

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"

@image.route('/stitch/<img>', methods=['GET'])
def stitch_images(img):
    # Recupera a lista de imagens enviada na requisição
    images = request.files.getlist(img)

    # Lê as imagens em memória usando OpenCV
    images_data = [cv2.imdecode(np.fromstring(image.read(), np.uint8), cv2.IMREAD_COLOR) for image in images]

    # Faz o stitch das imagens
    stitcher = cv2.createStitcher() if cv2.__version__.startswith('3') else cv2.Stitcher_create()
    status, stitched_image = stitcher.stitch(images_data)

     # Verificação do status da costura
    if status == 0:
        # Conversão da imagem resultante para um objeto de resposta
        _, buffer = cv2.imencode('.jpg', stitched_image)
        response = Response(buffer.tobytes(), mimetype='image/jpeg')
        return response
    else:
        return 'Erro ao costurar imagens'