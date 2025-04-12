from flask import request, jsonify, Blueprint, Response

from ..queries.get_customers import GetCustomers
from ..commands.sync_customers import SyncCustomer
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
def get_customers():
    try:
        response, status_code = GetCustomers().execute()
        return response, status_code
    except Exception as e:
        return jsonify({'error': str(e)}), 500