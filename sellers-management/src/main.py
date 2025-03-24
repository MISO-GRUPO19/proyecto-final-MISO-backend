from dotenv import load_dotenv
from flask import Flask, request, jsonify
from .api.sellers import sellers
from .errors.errors import ApiError
import os
from .models.database import init_db

load_dotenv('./.env.development')
APP_PORT = int(os.getenv("APP_PORT", default=5000))

app = Flask(__name__)
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