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
    
        mock_customer = MagicMock()
        mock_customer.id = data['id']
        mock_customer.firstName = data['firstName']
        mock_customer.lastName = data['lastName']
        mock_customer.phoneNumber = data['phoneNumber']
        mock_customer.address = data['address']
        mock_customer.country = data['country']
        mock_customer.email = data['email']
        mock_customer.created_at = datetime.datetime.utcnow()
        mock_customer.updated_at = datetime.datetime.utcnow()
    
        mock_customers.query.filter_by.return_value.first.return_value = None
    
        mock_db_session.add = MagicMock()
    
        sync_customer = SyncCustomer(data)
        response = sync_customer.execute()
    
        mock_db_session.commit.assert_called_once()
        assert response == {'message': 'Customer synced successfully'}

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
    
        mock_db_session.add.side_effect = Exception("Database error")
    
        sync_customer = SyncCustomer(data)
        response = sync_customer.execute()
    
        mock_db_session.rollback.assert_called_once()
        assert response == {'error': 'Database error'}
