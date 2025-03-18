from flask import request, jsonify, Blueprint, Response
from ..commands.create_ai import CreateAI

ai = Blueprint('ai', __name__)

@ai.route('/ai', methods=['POST'])
def create_ai():
    data = request.get_json()

    result = CreateAI(data).execute()
    return jsonify(result), 201

@ai.route('/ai/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200