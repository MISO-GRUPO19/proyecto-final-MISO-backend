from flask import request, jsonify, Blueprint, Response
from ..commands.create_products import CreateProducts
from ..commands.create_massive_products import CreateMassiveProducts

products = Blueprint('products', __name__)

@products.route('/products', methods=['POST'])
def create_product():
    data = request.get_json()

    result = CreateProducts(data).execute()
    return jsonify(result), 201

@products.route('/upload_products', methods=['POST'])
def upload_products():
    file = request.files['file']
    result = CreateMassiveProducts(file).execute()
    return jsonify(result), 201


@products.route('/products/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200