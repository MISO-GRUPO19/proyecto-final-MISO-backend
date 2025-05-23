from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import jwt_required
from ..queries.get_customers import GetCustomers
from ..commands.sync_customers import SyncCustomer
from ..queries.get_customer_by_id import GetCustomerById
from ..queries.get_customer_by_email import GetCustomerByEmail

customers = Blueprint('customers', __name__)

@customers.route('/customers/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

@customers.route('/customers/sync', methods=['POST'])
def sync_customer():
    data = request.get_json()
    try:
        response = SyncCustomer(data).execute()
        if response.get('error'):
            return jsonify({'error': response['error']}), 400
        if response.get('message') == 'Customer synced successfully':
            return jsonify({'message': response['message']}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@customers.route('/customers', methods=['GET'])
@jwt_required()
def get_customers():
    try:
        response, status_code = GetCustomers().execute()
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@customers.route('/customers/<uuid:customer_id>', methods=['GET'])
@jwt_required()
def get_customer_by_id(customer_id):
    try:
        response, status_code = GetCustomerById(customer_id).execute()
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@customers.route('/customers/<string:customer_email>', methods=['GET'])
@jwt_required()
def get_customer_by_email(customer_email):
    try:
        response, status_code = GetCustomerByEmail(customer_email).execute()
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500