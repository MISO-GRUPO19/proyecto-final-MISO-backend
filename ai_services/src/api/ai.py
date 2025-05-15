from flask import request, jsonify, Blueprint
from ..commands.process_video import ProcessVideo, GetVideoResult
from ..commands.create_routes import CreatRoute
from ..errors.errors import InvalidData, InvalidDate
from flask_jwt_extended import jwt_required
ai = Blueprint('ai', __name__)

@ai.route('/ai', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return jsonify({"error": "No se encontró archivo de video"}), 400

    video = request.files['video']
    visit_id = request.form.get('visitId')

    if not visit_id:
        return jsonify({"error": "Falta el visitId"}), 400

    response = ProcessVideo(video, visit_id).execute()
    return jsonify(response), 202

@ai.route('/ai/result/<video_id>', methods=['GET'])
def get_video_result(video_id):
    result = GetVideoResult(video_id).execute()
    return jsonify(result), 200


@ai.route('/ai/routes', methods=['POST'])
@jwt_required()
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
