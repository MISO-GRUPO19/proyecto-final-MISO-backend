from flask import request, jsonify, Blueprint, Response
from ..commands.create_customers import CreateCustomers

customers = Blueprint('customers', __name__)

@customers.route('/customers', methods=['POST'])
def create_customers():
    data = request.get_json()

    result = CreateCustomers(data).execute()
    return jsonify(result), 201

@customers.route('/customers/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200