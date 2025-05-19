from flask import request, jsonify, Blueprint
from ..commands.update_stock_products import UpdateStockProducts
from ..queries.get_product_validate import GetProductValidate

from ..commands.create_products import CreateProducts
from ..queries.get_product_by_id import GetById
from ..commands.create_massive_products import CreateMassiveProducts
from flask_jwt_extended import jwt_required
from ..queries.get_products import GetProducts
from ..errors.errors import InvalidData, ProductNotFound, ProductInsufficientStock
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
        return jsonify({"error": f"{e}Ocurrió un error inesperado"}), 500

@products.route('/products/upload_products', methods=['POST'])
@jwt_required()
def upload_products():
    file = request.files['file']
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    result = CreateMassiveProducts(file, auth_token).execute()
    
    return jsonify(result[0]), result[1]

@products.route('/products/<identification>/warehouses', methods=['GET'])
@jwt_required()
def get_product(identification):
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return GetById(identificator=identification, token=auth_token).execute()

@products.route('/products', methods=['GET'])
@jwt_required()
def get_products():
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    result = GetProducts(auth_token).execute()
    return jsonify(result), 200

@products.route('/products/info/<barcode>', methods=['GET'])
@jwt_required()
def get_product_info_by_barcode(barcode):
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    return GetById(barcode, auth_token).execute()

@products.route('/products/<barcode>', methods=['GET'])
@jwt_required()
def get_product_by_barcode(barcode):
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    quantity = request.args.get('quantity')
    
    return GetProductValidate(barcode=barcode, quantity=quantity, token=auth_token).execute()

@products.route('/products/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200


@products.route('/products/<barcode>', methods=['PUT'])
@jwt_required()
def update_product(barcode):
    quantity = request.args.get('quantity')

    try:
        result = UpdateStockProducts(barcode=barcode, quantity=quantity).execute()
        if result == ProductNotFound:
            return jsonify({"error": "Producto no encontrado"}), 404
        elif result == ProductInsufficientStock:
            return jsonify({"error": "Stock insuficiente"}), 400
        else:
            return jsonify(result), 200
    except InvalidData as e:
        return jsonify({"error": "Datos inválidos", "detalles": e.errors}), 400
    except Exception as e:
        return jsonify({"error": f"{e}Ocurrió un error inesperado"}), 500