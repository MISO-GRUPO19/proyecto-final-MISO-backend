from flask import request, jsonify, Blueprint, Response
from ..commands.create_orders import CreateOrders
from ..queries.get_orders import GetOrders

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['POST'])
def create_sale():
    data = request.get_json()
    
    fields = ['client_id', 'seller_id', 'date', 'provider_id', 'total', 'type', 'route_id', 'products']
    
    for field in fields:
        if field not in data:
            data[field] = ""
            
    result = CreateOrders(data['client_id'], data['seller_id'], data['date'], data['provider_id'], data['total'], data['type'], data['route_id'], data['products']).execute()
    return jsonify(result), 201

@orders.route('/orders', methods=['GET'])
def get_orders():
    token_beare = request.headers.get('Authorization')
    
    if token_beare is None:
        token = ""
    else:
        token = token_beare.replace('Bearer ', '')
        result = GetOrders(token).execute()
        return jsonify(result), 200
    
@orders.route('/orders/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200