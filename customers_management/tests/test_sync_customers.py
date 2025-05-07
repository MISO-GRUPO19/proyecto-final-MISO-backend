import datetime
from unittest import TestCase
from unittest.mock import MagicMock, patch, call, ANY
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
            'email': fake.email(),
            'seller_id': fake.uuid4()  
        }

        mock_customers.query.filter_by.return_value.first.return_value = None

        mock_new_customer = MagicMock()
        mock_customers.return_value = mock_new_customer

        mock_db_session.add = MagicMock()
        mock_db_session.commit = MagicMock()

        sync_customer = SyncCustomer(data)
        response = sync_customer.execute()

        mock_customers.assert_called_once_with(
            id=data['id'],
            firstName=data['firstName'],
            lastName=data['lastName'],
            phoneNumber=data['phoneNumber'],
            address=data['address'],
            country=data['country'],
            email=data['email'],
            seller_assigned=data['seller_id'],
            created_at=ANY,  
            updated_at=ANY   
        )

        mock_db_session.add.assert_called_once_with(mock_new_customer)
        mock_db_session.commit.assert_called_once()

        assert response == {'message': 'Customer synced successfully'}

    @patch('customers_management.src.commands.sync_customers.Customers')
    @patch('customers_management.src.commands.sync_customers.db_session')
    def test_sync_customer_exception(self, mock_db_session, mock_customers):
        data = {
            'id': fake.uuid4(),
            'firstName': fake.first_name(),
            'lastName': fake.last_name(),
            'phoneNumber': fake.phone_number(),
            'address': fake.address(),
            'country': fake.country(),
            'email': fake.email(),
            'seller_id': fake.uuid4()  
        }
        
        mock_db_session.commit.side_effect = Exception("Database error")
        mock_db_session.rollback = MagicMock()
        
        sync_customer = SyncCustomer(data)
        response = sync_customer.execute()
        
        mock_db_session.rollback.assert_called_once()
        
        self.assertEqual(response, {'error': 'Database error'})