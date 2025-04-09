from unittest.mock import patch, MagicMock
import pandas as pd
from datetime import datetime
from products_management.src.commands.create_massive_products import CreateMassiveProducts
import unittest

class TestCreateMassiveProducts(unittest.TestCase):
    @patch('products_management.src.pubsub.publisher.pubsub_v1.PublisherClient')  # Mockear el cliente de Pub/Sub
    @patch('products_management.src.pubsub.publisher.publish_message')  # Mockear la función que lo usa
    @patch('products_management.src.commands.create_massive_products.db_session')
    @patch('pandas.read_excel')
    @patch('products_management.src.commands.create_massive_products.requests.get')  # Mockear las solicitudes HTTP
    def test_execute_success(self, mock_requests_get, mock_read_excel, mock_db_session, mock_publish_message, mock_publisher_client):
        mock_publish_message.return_value = None  # Evita que se haga la llamada real

        mock_file = MagicMock()
        mock_file.filename = 'test.xlsx'

        mock_df = pd.DataFrame({
            'name': ['Valid', 'Valid Product'],
            'description': ['Description1', 'Description2'],
            'price': [19.0, 20.0],
            'category': ['Lácteos y Huevos', 'Condimentos y Especias'],
            'weight': [1.0, 2.0],
            'barcode': ['1234567890123', '1234567890124'],
            'provider': ['Provider1', 'Provider2'],
            'batch': ['Batch001', 'Batch002'],
            'best_before': [pd.Timestamp('2025-12-31'), pd.Timestamp('2025-10-31')],
            'quantity': [100, 200]
        })
        mock_read_excel.return_value = mock_df

        # Simular respuesta HTTP para validar proveedores
        mock_requests_get.return_value.status_code = 200
        mock_requests_get.return_value.json.return_value = {"id": "valid-uuid"}

        auth_token = "mocked-auth-token"  # Token simulado
        command = CreateMassiveProducts(mock_file, auth_token)  # Incluye el token
        result = command.execute()

        self.assertEqual(result[0]['message'], '2 productos cargados correctamente')
        
    @patch('products_management.src.pubsub.publisher.publish_message')
    @patch('products_management.src.commands.create_massive_products.db_session')
    @patch('pandas.read_excel')
    @patch('products_management.src.commands.create_massive_products.requests.get')  # Mockear las solicitudes HTTP
    def test_execute_with_invalid_data(self, mock_requests_get, mock_read_excel, mock_db_session, mock_publish_message):
        mock_file = MagicMock()
        mock_file.filename = 'test.xlsx'

        mock_df = pd.DataFrame({
            'name': ['', ''],
            'description': ['Description1', 'Description2'],
            'price': ['Invalid', 'Invalid'],
            'category': ['Condimentos y Especias', 'Condimentos y Especias'],
            'weight': [1.0, 2.0],
            'barcode': ['1234567890123', '1234567890124'],
            'provider': ['invalid-uuid', 'invalid-uuid'],
            'batch': ['Batch001', 'Batch002'],
            'best_before': [pd.Timestamp('2025-12-31'), pd.Timestamp('2025-10-31')],
            'quantity': [100, 200]
        })
        mock_read_excel.return_value = mock_df

        mock_db_session.query.return_value.filter_by.return_value.first.return_value = None

        # Simular respuesta HTTP para validar proveedores
        mock_requests_get.return_value.status_code = 404  # Proveedor no encontrado
        mock_requests_get.return_value.json.return_value = {"error": "Provider not found"}

        auth_token = "mocked-auth-token"  # Token simulado
        command = CreateMassiveProducts(mock_file, auth_token)  # Incluye el token
        result = command.execute()

        self.assertIn('errores en la carga', result[0]['message'].lower())
        self.assertEqual(len(result[0]), len(mock_df))
        mock_publish_message.assert_not_called()