import cv2
from flask import Flask, Blueprint, request, jsonify

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"

@image.route('/stitch/<img>', methods=['POST'])
def stitch_images(img):
     # Obtém a lista de arquivos da solicitação
    files = request.files.getlist('img')
    
    # Salva os arquivos temporariamente no servidor
    image_paths = []
    for file in files:
        filename = secure_filename(file.filename)
        image_path = os.path.join('/tmp', filename)
        file.save(image_path)
        image_paths.append(image_path)

    # Faz a costura das imagens usando OpenCV
    stitched_image = None
    for image_path in image_paths:
        image = cv2.imread(image_path)
        if stitched_image is None:
            stitched_image = image
        else:
            stitched_image = cv2.addWeighted(stitched_image, 0.5, image, 0.5, 0)

    # Salva a imagem costurada em um arquivo temporário
    stitched_image_path = os.path.join('/tmp', 'stitched.jpg')
    cv2.imwrite(stitched_image_path, stitched_image)

    # Retorna o arquivo de imagem costurada como uma resposta HTTP
    return stitched_image_path