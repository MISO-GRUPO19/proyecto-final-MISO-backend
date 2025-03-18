from flask import request, jsonify, Blueprint, Response
from ..commands.create_users import CreateUsers

users = Blueprint('users', __name__)

@users.route('/users', methods=['POST'])
def create_users():
    data = request.get_json()

    result = CreateUsers(data).execute()
    return jsonify(result), 201

@users.route('/users/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200