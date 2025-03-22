from flask import request, jsonify, Blueprint
from ..commands.create_users import CreateUsers
from ..commands.login_user import LoginUserCommand
from ..errors.errors import InvalidData
from ..commands.create_customer import CreateCustomer
users = Blueprint('users', __name__)

@users.route('/users', methods=['POST'])
def create_users():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        raise InvalidData()

    result = CreateUsers(data).execute()
    return jsonify(result), 201

@users.route('/customers', methods=['POST'])
def create_customers():
    data = request.get_json()

    if not data or 'name' not in data or 'country' not in data or 'address' not in data or 'telephone' not in data or 'email' not in data:
        raise InvalidData()

    result = CreateCustomer(data).execute()
    return jsonify(result), 201

@users.route('/users/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'email' not in data or 'password' not in data:
        raise InvalidData()

    email = data.get('email').strip().lower()
    password = data.get('password')

    result = LoginUserCommand(email, password).execute()
    
    return jsonify(result), 200

@users.route('/users/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200

