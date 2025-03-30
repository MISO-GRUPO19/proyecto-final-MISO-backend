from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from .api.sellers import sellers
from .errors.errors import ApiError
import os
from .models.database import init_db
from flask_cors import CORS

load_dotenv('./.env.development')
APP_PORT = int(os.getenv("APP_PORT", default=5000))

app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "qwerty"
jwt = JWTManager(app)
app.register_blueprint(sellers)

init_db()

@app.errorhandler(ApiError)
def handle_exception(error):
    response = {
      "mssg": error.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), error.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT)