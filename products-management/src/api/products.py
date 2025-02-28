from flask import request, jsonify, Blueprint, Response
from ..commands.create_products import CreateProducts

products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    result = CreateProducts(data).execute()
    return jsonify(result), 201

@products.route('/products/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200