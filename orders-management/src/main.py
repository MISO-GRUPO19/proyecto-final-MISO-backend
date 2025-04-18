from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_jwt_extended import JWTManager
from .api.orders import orders
from .errors.errors import ApiError
import os
from .models.database import init_db
import uptrace

# Inicializar Uptrace
uptrace.configure_opentelemetry(
    dsn="https://t0Yfk4-x00bJJt5WlUqreg@api.uptrace.dev/5872",
    service_name="orders-management",
    service_version="1.0.0",
)

load_dotenv('./.env.development')
APP_PORT = int(os.getenv("APP_PORT", default=5000))

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "qwerty"  # Debe ser la misma clave secreta usada en el servicio de autenticación
jwt = JWTManager(app)

app.register_blueprint(orders)

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