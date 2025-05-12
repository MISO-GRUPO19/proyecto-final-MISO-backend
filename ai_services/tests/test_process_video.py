import unittest
from unittest.mock import patch, MagicMock, ANY
import uuid
from io import BytesIO
from ai_services.src.models.video import Video, VideoStatus
from ai_services.src.commands.process_video import ProcessVideo, GetVideoResult


class TestProcessVideo(unittest.TestCase):
    @patch('ai_services.src.commands.process_video.publish_message')
    @patch('ai_services.src.commands.process_video.db_session')
    @patch('google.cloud.storage.Client') 
    def test_execute_success(self, mock_storage_client, mock_db_session, mock_publish):
        # Mock de archivo
        mock_file = MagicMock()
        mock_file.filename = "test.mp4"
        mock_file.content_type = "video/mp4"
        mock_file.stream = BytesIO(b"test video content")

        # Mock de storage
        mock_blob = MagicMock()
        mock_blob.public_url = "http://storage.test/video123.mp4"
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value.bucket.return_value = mock_bucket

        # Mock de base de datos
        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        visit_id = uuid.uuid4()

        processor = ProcessVideo(mock_file, visit_id)
        result = processor.execute()

        self.assertIn("video_id", result)
        self.assertEqual(result["status"], "PROCESANDO")
        mock_blob.upload_from_file.assert_called_once()
        mock_db_session.add.assert_called_once()
        mock_db_session.commit.assert_called_once()
        mock_publish.assert_called_once_with('videos', {'video_id': ANY})

    @patch('google.cloud.storage.Client') 
    def test_upload_to_gcs(self, mock_storage_client):
        mock_file = MagicMock()
        mock_file.stream = BytesIO(b"test content")
        mock_file.content_type = "video/mp4"

        mock_blob = MagicMock()
        mock_blob.public_url = "http://test.url"
        mock_bucket = MagicMock()
        mock_bucket.blob.return_value = mock_blob
        mock_storage_client.return_value.bucket.return_value = mock_bucket

        processor = ProcessVideo(None, None)
        url = processor.upload_to_gcs(mock_file, "test_path.mp4")

        self.assertEqual(url, "http://test.url")
        mock_blob.upload_from_file.assert_called_once()


class TestGetVideoResult(unittest.TestCase):
    @patch('ai_services.src.commands.process_video.db_session')
    def test_execute_video_found(self, mock_db_session):
        video_id = uuid.uuid4()
        visit_id = uuid.uuid4()

        mock_video = MagicMock()
        mock_video.id = video_id
        mock_video.status = VideoStatus.processed
        mock_video.results = {"emotion": "happy"}

        mock_db_session.query.return_value.filter_by.return_value.first.return_value = mock_video

        getter = GetVideoResult(visit_id)
        result = getter.execute()

        self.assertEqual(result["video_id"], video_id)
        self.assertEqual(result["status"], "PROCESADO")
        self.assertEqual(result["result"], {"emotion": "happy"})

    @patch('ai_services.src.commands.process_video.db_session')
    def test_execute_video_not_found(self, mock_db_session):
        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        getter = GetVideoResult(uuid.uuid4())
        result = getter.execute()

        self.assertEqual(result, {"error": "Video no encontrado"})


class TestVideoModel(unittest.TestCase):
    def test_video_creation(self):
        visit_id = uuid.uuid4()

        video = Video(
            fileInfo="http://test.url",
            name="test.mp4",
            visitId=visit_id,
            status=VideoStatus.processing
        )

        self.assertEqual(video.fileInfo, "http://test.url")
        self.assertEqual(video.name, "test.mp4")
        self.assertEqual(video.visitId, visit_id)
        self.assertEqual(video.status, VideoStatus.processing)
        self.assertIsNone(video.results)
