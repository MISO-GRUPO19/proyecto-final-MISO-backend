from flask import request, jsonify, Blueprint, Response

from ..queries.get_categories import GetCategories
from ..commands.create_products import CreateProducts
from ..commands.create_massive_products import CreateMassiveProducts
from flask_jwt_extended import jwt_required, get_jwt_identity

products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
@jwt_required()
def create_product():
    data = request.get_json()

    result = CreateProducts(data).execute()
    return jsonify(result), 201

@products.route('/products/upload_products', methods=['POST'])
@jwt_required()
def upload_products():
    file = request.files['file']
    result = CreateMassiveProducts(file).execute()
    return jsonify(result), 201

@products.route('/categories', methods=['GET'])
@jwt_required()
def get_categories():
    result = GetCategories(get_jwt_identity()).execute()
    return jsonify(result), 200

@products.route('/products/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200