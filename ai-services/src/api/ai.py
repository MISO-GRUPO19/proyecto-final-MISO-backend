from flask import request, jsonify, Blueprint, Response
from ..commands.create_ai import CreateAI
from ..commands.create_routes import CreatRoute
from ..errors.errors import InvalidData, InvalidDate

ai = Blueprint('ai', __name__)

@ai.route('/ai', methods=['POST'])
def create_ai():
    data = request.get_json()

    result = CreateAI(data).execute()
    return jsonify(result), 201

@ai.route('/ai/routes', methods=['POST'])
def create_routes():
    auth_token = request.headers.get("Authorization", "").replace("Bearer ", "")
    data = request.get_json()
    try:
        result = CreatRoute(data, auth_token).execute()
        return jsonify(result), 201
    except InvalidData as e:
        return jsonify({"error": e.description}), 400
    except InvalidDate as e:
        return jsonify({"error": e.description}), 400
    except Exception as e:
        return jsonify({"error": "An unexpected error occurred", "details": str(e)}), 500


@ai.route('/ai/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200
