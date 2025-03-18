from flask import request, jsonify, Blueprint, Response
from ..commands.create_manufacturers import CreateManufacturers

manufacturers = Blueprint('manufacturers', __name__)

@manufacturers.route('/manufacturers', methods=['POST'])
def create_manufacturers():
    data = request.get_json()

    result = CreateManufacturers(data).execute()
    return jsonify(result), 201

@manufacturers.route('/manufacturers/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200