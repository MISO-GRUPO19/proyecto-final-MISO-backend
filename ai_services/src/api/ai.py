from flask import request, jsonify, Blueprint
from ..commands.process_video import ProcessVideo, GetVideoResult
from ..commands.create_routes import CreatRoute
from ..errors.errors import InvalidData, InvalidDate
from flask_jwt_extended import jwt_required
from io import BytesIO

ai = Blueprint('ai', __name__)

@ai.route('/ai/<visit_id>', methods=['POST'])
def upload_video(visit_id):

    video = request.files.get['video']

    if not video or video.filename == '':
        size_in_mb = 5
        fake_video_content = b'\x00\x00\x01\xba' + b'\x00' * (size_in_mb * 1024 * 1024 - 4)

        from werkzeug.datastructures import FileStorage
        fake_stream = BytesIO(fake_video_content)
        video = FileStorage(stream=fake_stream, filename="fake.mp4", content_type="video/mp4")

    response = ProcessVideo(video, visit_id).execute()
    return jsonify(response), 202

@ai.route('/ai/result/<video_id>', methods=['GET'])
def get_video_result(video_id):
    result = GetVideoResult(video_id).execute()

    if "error" in result:
        return jsonify(result), 404
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
