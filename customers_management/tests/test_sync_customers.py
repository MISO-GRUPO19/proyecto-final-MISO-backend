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
        'seller_id': fake.uuid4()  # Added seller_id which was missing
    }

    # Setup mock customer query to return None (customer doesn't exist)
    mock_customers.query.filter_by.return_value.first.return_value = None

    # Create a fresh MagicMock for the customer instance
    mock_new_customer = MagicMock()
    mock_customers.return_value = mock_new_customer

    # Setup the db_session mock
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    sync_customer = SyncCustomer(data)
    response = sync_customer.execute()

    # Verify the customer was created with correct data
    mock_customers.assert_called_once_with(
        id=data['id'],
        firstName=data['firstName'],
        lastName=data['lastName'],
        phoneNumber=data['phoneNumber'],
        address=data['address'],
        country=data['country'],
        email=data['email'],
        seller_assigned=data['seller_id'],
        created_at=ANY,  # Ignore the value of created_at
        updated_at=ANY   # Ignore the value of updated_at
    )

    # Verify database operations
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
            'seller_id': fake.uuid4()  # Added seller_id
        }
        
        # Setup mock to raise exception on commit
        mock_db_session.commit.side_effect = Exception("Database error")
        mock_db_session.rollback = MagicMock()
        
        sync_customer = SyncCustomer(data)
        response = sync_customer.execute()
        
        # Verify rollback was called
        mock_db_session.rollback.assert_called_once()
        
        # Verify error response format
        self.assertEqual(response, {'error': 'Database error'})