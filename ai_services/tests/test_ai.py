import io
from unittest.mock import patch
from flask import Flask
from ai_services.src.api.ai import ai
import unittest


class TestAiRoutes(unittest.TestCase):
    def setUp(self):
        app = Flask(__name__)
        app.register_blueprint(ai)
        self.client = app.test_client()

    def test_ping(self):
        response = self.client.get('/ai/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {'message': 'pong'})

    def test_upload_video_missing_file(self):
        response = self.client.post('/ai', data={})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "No se encontró archivo de video"})

    def test_upload_video_missing_visit_id(self):
        fake_file = (io.BytesIO(b"fake content"), 'test.mp4')
        data = {
            'video': fake_file
        }
        response = self.client.post('/ai', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"error": "Falta el visitId"})

    @patch('ai_services.src.api.ai.ProcessVideo')
    def test_upload_video_success(self, mock_process):
        mock_process.return_value.execute.return_value = {
            "video_id": "123",
            "status": "PROCESANDO"
        }

        fake_file = (io.BytesIO(b"fake content"), 'test.mp4')
        data = {
            'video': fake_file,
            'visitId': 'some-uuid'
        }
        response = self.client.post('/ai', data=data, content_type='multipart/form-data')
        self.assertEqual(response.status_code, 202)
        self.assertEqual(response.get_json(), {
            "video_id": "123",
            "status": "PROCESANDO"
        })

    @patch('ai_services.src.api.ai.GetVideoResult')
    def test_get_video_result(self, mock_getter):
        mock_getter.return_value.execute.return_value = {
            "video_id": "123",
            "status": "PROCESADO",
            "result": {"emotion": "happy"}
        }

        response = self.client.get('/ai/result/123')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {
            "video_id": "123",
            "status": "PROCESADO",
            "result": {"emotion": "happy"}
        })
