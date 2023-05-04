import cv2
from flask import Flask, Blueprint, request, jsonify

image = Blueprint('image',__name__)

@image.route('/')
def instructions():
    return "Image"

@image.route('/stitch')
def stitch_images():
    return 'Verdade'