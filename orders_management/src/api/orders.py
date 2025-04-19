from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..commands.create_orders import CreateOrders
from ..queries.get_order_by_client import GetOrderByClient
from uuid import UUID

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['POST'])
@jwt_required()
def create_sale():
    data = request.get_json()
    
    fields = ['client_id', 'seller_id', 'date', 'provider_id', 'total', 'type', 'route_id', 'products']
    
    for field in fields:
        if field not in data:
            data[field] = ""

    try:
        client_id = UUID(data['client_id'])
        seller_id = UUID(data['seller_id'])
        provider_id = UUID(str(data['provider_id']))
        route_id = UUID(str(data['route_id']))
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid UUID format: {e}"}), 400
    
    token_beare = request.headers.get('Authorization')
    
    if token_beare is None:
        token = ""
    else:
        token = token_beare.replace('Bearer ', '')
             
    result = CreateOrders(token, client_id, seller_id, data['date'], provider_id, data['total'], data['type'], route_id, data['products']).execute()
    return jsonify(result), 201

@orders.route('/orders/<client_id>', methods=['GET'])
@jwt_required()
def get_orders(client_id):
    token_beare = request.headers.get('Authorization')
    
    if token_beare is None:
        token = ""
    else:
        token = token_beare.replace('Bearer ', '')
        result = GetOrderByClient(token, client_id).execute()
        return jsonify(result), 200
    
@orders.route('/orders/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200