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
