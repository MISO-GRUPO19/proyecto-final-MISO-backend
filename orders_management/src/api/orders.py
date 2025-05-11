from flask import request, jsonify, Blueprint, Response
from flask_jwt_extended import jwt_required, get_jwt_identity
from ..commands.create_orders import CreateOrders
from ..queries.get_order_by_client import GetOrderByClient
from ..queries.get_order_by_id import GetOrderById
from ..commands.update_orders import UpdateStateOrder
from ..commands.generate_seller_visits import GenerateSellerVisits
from uuid import UUID
from ..commands.update_visit import UpdateVisit
from ..errors.errors import InvalidData, ProductInsufficientStock, ProductNotFound, GoalNotFound
from ..commands.create_seller_goals import CreateSellerGoals
from ..queries.get_seller_sales_by_id import GetSellerSalesById

orders = Blueprint('orders', __name__)

@orders.route('/orders', methods=['POST'])
@jwt_required()
def create_sale():
    data = request.get_json()
    
    fields = ['client_id', 'date', 'total', 'type', 'products']
    
    for field in fields:
        if field not in data:
            data[field] = ""

    try:
        client_id = UUID(data['client_id'])
        seller_id = UUID(data.get('seller_id')) if data.get('seller_id') else None
        provider_id = UUID(data.get('provider_id')) if data.get('provider_id') else None
        route_id = UUID(data.get('route_id')) if data.get('route_id') else None
    except (ValueError, TypeError) as e:
        return jsonify({"error": f"Invalid UUID format: {e}"}), 400
    
    token_beare = request.headers.get('Authorization')
    
    if token_beare is None:
        token = ""
    else:
        token = token_beare.replace('Bearer ', '')
         
    try:    
        result = CreateOrders(token, client_id, seller_id, data['date'], provider_id, data['total'], data['type'], route_id, data['products']).execute()
        return result
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@orders.route('/orders/<client_id>', methods=['GET'])
@jwt_required()
def get_orders(client_id):
    token_beare = request.headers.get('Authorization')
    
    if token_beare is None:
        token = ""
    else:
        try:
            token = token_beare.replace('Bearer ', '')
            result = GetOrderByClient(token, client_id).execute()
            return jsonify(result), 200
        except InvalidData as e:
            return jsonify({"error": e.description}), 400
        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@orders.route('/orders/order/<order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    token_beare = request.headers.get('Authorization')
    
    if token_beare is None:
        token = ""
    else:
        token = token_beare.replace('Bearer ', '')
        result = GetOrderById(token, order_id).execute()
        
    if not result:
        return jsonify({"error": "Order not found"}), 404
    else:
        return jsonify(result), 200

@orders.route('/orders/<order_id>/status', methods=['PUT'])
@jwt_required()
def update_order_status(order_id):
    token_beare = request.headers.get('Authorization')    
    try:
        if token_beare is None:
            token = ""
        else:
            token = token_beare.replace('Bearer ', '')
            result = UpdateStateOrder(token, order_id, request.json['state']).execute()
            return jsonify(result), 200
    except InvalidData as e:
        return jsonify({"error": e.description}), 400
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@orders.route('/orders/visits/<seller_id>', methods=['GET'])
def generate_seller_visits(seller_id):
    try:
        result = GenerateSellerVisits(seller_id).execute()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500

@orders.route('/orders/goals', methods=['POST'])
def create_goal_sales():
    data = request.get_json()
    try:
        result = CreateSellerGoals(data).execute()
        return jsonify(result), 201
    except Exception as e:
        return jsonify({"error": f"An unexpected error occurred: {e}"}), 500    
    
@orders.route('/orders/visit/<visit_id>', methods=['PUT'])
@jwt_required()
def update_visit(visit_id):
    token_beare = request.headers.get('Authorization')
    
    if token_beare is None:
        token = ""
    else:
        token = token_beare.replace('Bearer ', '')
        try:
            result = UpdateVisit(token, visit_id, request.json['state']).execute()
            return jsonify(result), 200
        except InvalidData as e:
            return jsonify({"error": e.description}), 400
        except Exception as e:
            return jsonify({"error": f"An unexpected error occurred: {e}"}), 500
              

@orders.route('/orders/sellers/<seller_id>/sales', methods=['GET'])
@jwt_required()
def get_seller_sales(seller_id):
    try:
        result = GetSellerSalesById(seller_id).execute()
        return jsonify(result), 200
    except GoalNotFound as e:
        return jsonify({"error": e.description}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@orders.route('/orders/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200