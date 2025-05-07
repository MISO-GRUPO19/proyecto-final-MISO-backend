import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch
from faker import Faker
from customers_management.src.commands.sync_customers import SyncCustomer

fake = Faker()

class TestSyncCustomer(TestCase):

    @patch('customers_management.src.commands.sync_customers.Customers')
    @patch('customers_management.src.commands.sync_customers.Stores')
    @patch('customers_management.src.commands.sync_customers.db_session')
    def test_sync_customer_create(self, mock_db_session, mock_stores, mock_customers):
        data = {
            'id': fake.uuid4(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'phoneNumber': fake.phone_number(),
            'address': fake.address(),
            'country': fake.country(),
            'email': fake.email()
        }

        # Configurar mocks
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session  # Cambio clave aquí
        mock_customers.query.filter_by.return_value.first.return_value = None
        
        sync_customer = SyncCustomer(data)
        response = sync_customer.execute()  # Ahora solo recibe el diccionario
        
        # Verificar llamadas
        self.assertEqual(response, {'message': 'Customer synced successfully'})
        mock_session.commit.assert_called_once()

    @patch('customers_management.src.commands.sync_customers.db_session')
    def test_sync_customer_exception(self, mock_db_session):
        data = {
            'id': fake.uuid4(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'phoneNumber': fake.phone_number(),
            'address': fake.address(),
            'country': fake.country(),
            'email': fake.email()
        }

        # Configurar mock para excepción
        mock_session = MagicMock()
        mock_db_session.return_value = mock_session  # Cambio clave aquí
        mock_session.add.side_effect = Exception("Database error")
        
        sync_customer = SyncCustomer(data)
        response = sync_customer.execute()  # Ahora solo recibe el diccionario
        
        # Verificar llamadas
        self.assertEqual(response, {'error': 'Database error'})
        mock_session.rollback.assert_called_once()