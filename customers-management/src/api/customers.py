from flask import request, jsonify, Blueprint, Response

customers = Blueprint('customers', __name__)

@customers.route('/customers/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200