import unittest
from unittest.mock import patch, MagicMock
from ai_services.src.pubsub.publisher import publish_message


class TestPublishMessage(unittest.TestCase):
    @patch('ai_services.src.pubsub.publisher.pubsub_v1.PublisherClient')
    def test_publish_message_success(self, mock_publisher_client):
        # Arrange
        mock_publisher = MagicMock()
        mock_future = MagicMock()
        mock_future.result.return_value = 'mock-message-id'
        mock_publisher.publish.return_value = mock_future
        mock_publisher.topic_path.return_value = 'projects/proyecto-final-451719/topics/test-topic'
        mock_publisher_client.return_value = mock_publisher

        data = {'video_id': '123', 'status': 'PROCESANDO'}

        # Act
        publish_message('test-topic', data)

        # Assert
        mock_publisher.topic_path.assert_called_once_with('proyecto-final-451719', 'test-topic')
        mock_publisher.publish.assert_called_once()
        args, kwargs = mock_publisher.publish.call_args
        assert args[0] == 'projects/proyecto-final-451719/topics/test-topic'
        assert args[1] == b'{"video_id": "123", "status": "PROCESANDO"}'
        mock_future.result.assert_called_once()
