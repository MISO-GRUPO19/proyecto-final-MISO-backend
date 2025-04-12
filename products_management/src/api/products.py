from flask import request, jsonify, Blueprint

from ..commands.create_products import CreateProducts
from ..commands.create_massive_products import CreateMassiveProducts
from flask_jwt_extended import jwt_required
from ..queries.get_products import GetProducts
from ..errors.errors import InvalidData
products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    try:
        result = CreateProducts(data, auth_token).execute()
        return jsonify(result), 201
    except InvalidData as e:
        return jsonify({"error": "Datos inválidos", "detalles": e.errors}), 400
    except Exception as e:
        return jsonify({"error": "Ocurrió un error inesperado"}), 500

@products.route('/products/upload_products', methods=['POST'])
@jwt_required()
def upload_products():
    file = request.files['file']
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    result = CreateMassiveProducts(file, auth_token).execute()
    
    return jsonify(result[0]), result[1]

@products.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    result = GetProducts(auth_token).execute()
    return jsonify(result), 200


@products.route('/products/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200