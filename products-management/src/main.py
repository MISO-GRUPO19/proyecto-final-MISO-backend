from dotenv import load_dotenv
from flask import Flask, request, jsonify
from .api.products import products
from .errors.errors import ApiError
import os
from .models.database import init_db
import uptrace

# Inicializar Uptrace
uptrace.configure_opentelemetry(
    dsn="https://t0Yfk4-x00bJJt5WlUqreg@api.uptrace.dev/5872",
    service_name="products-management",
    service_version="1.0.0",
)

load_dotenv('./.env.development')
APP_PORT = int(os.getenv("APP_PORT", default=5000))

app = Flask(__name__)
app.register_blueprint(products)

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