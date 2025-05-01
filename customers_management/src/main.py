from dotenv import load_dotenv
from flask import Flask, request, jsonify
from .api.customers import customers
from .errors.errors import ApiError
import os
from .models.database import init_db, db_session
import uptrace
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# Inicializar Uptrace
uptrace.configure_opentelemetry(
    dsn="https://t0Yfk4-x00bJJt5WlUqreg@api.uptrace.dev/5872",
    service_name="customers-management",
    service_version="1.0.0",
)
 
load_dotenv('./.env.development')
APP_PORT = int(os.getenv("APP_PORT", default=5000))


app = Flask(__name__)
CORS(app)

app.config["JWT_SECRET_KEY"] = "qwerty"
jwt = JWTManager(app)

app.config["DEBUG"] = True

app.register_blueprint(customers)

init_db()

@app.errorhandler(ApiError)
def handle_exception(error):
    response = {
      "mssg": error.description,
      "version": os.environ["VERSION"]
    }
    return jsonify(response), error.code

@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=APP_PORT)