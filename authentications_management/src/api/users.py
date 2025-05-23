from flask import request, jsonify, Blueprint
from ..commands.create_users import CreateUsers
from ..commands.login_user import LoginUserCommand
from ..commands.create_customer import CreateCustomer
from flask_jwt_extended import jwt_required
from ..commands.create_sellers import CreateSellers
from ..errors.errors import *
from ..queries.get_seller_by_id import GetSellersById
from ..queries.get_seller_by_identification import GetSellerByIdentification
from ..queries.get_sellers import GetSellers
from ..commands.assign_customer_to_seller import AssignCustomerToSeller
users = Blueprint('users', __name__)

@users.route('/users', methods=['POST'])
def create_users():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        raise InvalidData()

    result = CreateUsers(data).execute()
    return jsonify(result), 201

@users.route('/users/customers', methods=['POST'])
def create_customers():
    data = request.get_json()
    if not data or 'firstName' not in data or 'lastName' not in data or 'country' not in data or 'address' not in data or 'phoneNumber' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid data provided'}), 400

    try:
        result = CreateCustomer(data).execute()
        return jsonify(result), 201
    except InvalidData as e:
        return jsonify({'error': e.description}), 400
    except EmailDoesNotValid as e:
        return jsonify({'error': e.description}), 400
    except UserAlreadyExists as e:
        return jsonify({'error': e.description}), 409
    except InvalidNameCustomer as e:
        return jsonify({'error': e.description}), 400
    except InvalidAddressCustomer as e:
        return jsonify({'error': e.description}), 400
    except InvalidTelephoneCustomer as e:
        return jsonify({'error': e.description}), 400
    except Exception as e:
        return jsonify({'error': 'An unexpected error occurred', 'details': str(e)}), 500

@users.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        raise InvalidData()

    email = data.get('email').strip().lower()
    password = data.get('password')

    result = LoginUserCommand(email, password).execute()
    
    return jsonify(result), 200
    
@users.route('/users/sellers', methods=['POST'])
@jwt_required()
def create_seller():
    data = request.get_json()
    try:
        result = CreateSellers(data).execute()
        return jsonify(result), 201
    except InvalidData as e:
        return jsonify({"error": e.description}), 400
    except InvalidIdentification as e:
        return jsonify({"error": e.description}), 400
    except InvalidName as e:
        return jsonify({"error": e.description}), 400
    except InvalidCountry as e:
        return jsonify({"error": e.description}), 400
    except InvalidAddress as e:
        return jsonify({"error": e.description}), 400
    except InvalidTelephone as e:
        return jsonify({"error": e.description}), 400
    except InvalidEmail as e:
        return jsonify({"error": e.description}), 400

@users.route('/users/sellers', methods=['GET'])
@jwt_required()
def get_sellers():
    try:
        result = GetSellers().execute()
        return jsonify(result), 200
    except SellerNotFound as e:
        return jsonify({"error": e.description}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@users.route('/users/sellers/<uuid:seller_id>', methods=['GET'])
@jwt_required()
def get_seller(seller_id):
    try:
        result = GetSellersById(seller_id).execute()
        return jsonify(result), 200
    except SellerNotFound as e:
        return jsonify({"error": e.description}), 404
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@users.route('/users/sellers/<string:seller_id>', methods=['GET'])
def get_seller_by_identification(seller_id):
    try:
        result = GetSellerByIdentification(seller_id).execute()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@users.route('/users/sellers/<seller_id>/customers', methods=['PUT'])
@jwt_required()
def assign_customer_to_seller(seller_id):
    data = request.get_json()
    try:
        result = AssignCustomerToSeller(data, seller_id).execute()
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500

@users.route('/users/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

