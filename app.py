# pip install pipenv
# pipenv install
# pip shell
from flask import Flask
from flask_cors import CORS

from api.image_service import image

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})

#
# REGISTRAR AS ROTAS
#
app.register_blueprint(image,url_prefix="/api/image")

@app.route("/")
def instructions():
    return "API Image"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)