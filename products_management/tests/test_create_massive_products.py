from unittest.mock import patch, MagicMock
import pandas as pd
import uuid
from datetime import datetime
from products_management.src.commands.create_massive_products import CreateMassiveProducts
from products_management.src.models.products import Category, Provider
import unittest

class TestCreateMassiveProducts(unittest.TestCase):
    @patch('products_management.src.pubsub.publisher.pubsub_v1.PublisherClient')  # Mockear el cliente de Pub/Sub
    @patch('products_management.src.pubsub.publisher.publish_message')  # Mockear la función que lo usa
    @patch('products_management.src.commands.create_massive_products.db_session')
    @patch('pandas.read_excel')
    def test_execute_success(self, mock_read_excel, mock_db_session, mock_publish_message, mock_publisher_client):
        mock_publish_message.return_value = None  # Evita que se haga la llamada real

        mock_file = MagicMock()
        mock_file.filename = 'test.xlsx'

        simulated_db = {
            "categories": {"Electronic": MagicMock(spec=Category)},
            "providers": {}
        }

        valid_provider = MagicMock(spec=Provider)
        valid_provider.id = str(uuid.uuid4())
        simulated_db["providers"][valid_provider.id] = valid_provider

        mock_df = pd.DataFrame({
            'name': ['Valid', 'Valid Product'],
            'description': ['Description1', 'Description2'],
            'price': [19.0, 20.0],
            'category': ['Electronic', 'Electronic'],
            'weight': [1.0, 2.0],
            'barcode': ['1234567890123', '1234567890124'],
            'provider_id': [valid_provider.id, valid_provider.id],
            'batch': ['Batch001', 'Batch002'],
            'best_before': [pd.Timestamp('2025-12-31'), pd.Timestamp('2025-10-31')],
            'quantity': [100, 200]
        })
        mock_read_excel.return_value = mock_df

        def query_side_effect(model):
            if model == Category:
                return MagicMock(filter_by=lambda name: MagicMock(first=lambda: simulated_db["categories"].get(name, None)))
            if model == Provider:
                return MagicMock(filter_by=lambda id: MagicMock(first=lambda: simulated_db["providers"].get(str(id), None)))
            return MagicMock()

        mock_db_session.query.side_effect = query_side_effect

        def add_side_effect(instance):
            if isinstance(instance, Provider):
                simulated_db["providers"][instance.id] = instance

        mock_db_session.add.side_effect = add_side_effect
        mock_db_session.commit.side_effect = lambda: None

        command = CreateMassiveProducts(mock_file)
        result = command.execute()


        assert result == {'message': '2 productos cargados correctamente'}

    @patch('products_management.src.pubsub.publisher.publish_message')
    @patch('products_management.src.commands.create_massive_products.db_session')
    @patch('pandas.read_excel')
    def test_execute_with_invalid_data(self, mock_read_excel, mock_db_session, mock_publish_message):
        mock_file = MagicMock()
        mock_file.filename = 'test.xlsx'

        mock_df = pd.DataFrame({
            'name': ['', ''],
            'description': ['Description1', 'Description2'],
            'price': ['Invalid', 'Invalid'],
            'category': ['InvalidCategory', 'InvalidCategory'],
            'weight': [1.0, 2.0],
            'barcode': ['1234567890123', '1234567890124'],
            'provider_id': ['invalid-uuid', 'invalid-uuid'],
            'batch': ['Batch001', 'Batch002'],
            'best_before': [pd.Timestamp('2025-12-31'), pd.Timestamp('2025-10-31')],
            'quantity': [100, 200]
        })
        mock_read_excel.return_value = mock_df

        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        command = CreateMassiveProducts(mock_file)
        result = command.execute()

        self.assertIn('errores en la carga', result['message'].lower())
        self.assertEqual(len(result['detalles']), len(mock_df))
        mock_publish_message.assert_not_called()
