from flask import request, jsonify, Blueprint
from ..commands.process_video import ProcessVideo, GetVideoResult

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


@ai.route('/ai/ping', methods=['GET'])
def ping():
    return jsonify({'message': 'pong'}), 200
