import pytest
from unittest.mock import patch, MagicMock
from authentications_management.src.commands.create_customer import CreateCustomer
from authentications_management.src.errors.errors import InvalidAddressCustomer, InvalidData, InvalidTelephoneCustomer, UserAlreadyExists, EmailDoesNotValid
import os
from authentications_management.src.errors.errors import InvalidData, UserAlreadyExists

@pytest.fixture
@patch('authentications_management.src.commands.create_customer.Customers')
@patch('authentications_management.src.commands.create_customer.db_session')
@patch('authentications_management.src.commands.create_customer.requests.post')
def test_create_customer_sync_service_called(mock_requests_post, mock_db_session, mock_customers, valid_data):
    mock_customers.query.filter_by.return_value.first.return_value = None
    mock_customer_instance = MagicMock()
    mock_customer_instance.id = 1
    mock_customers.return_value = mock_customer_instance

    mock_requests_post.return_value.status_code = 200

    command = CreateCustomer(valid_data)
    result = command.execute()

    assert result == {'message': 'Customer created successfully', 'customer_id': 1}
    mock_requests_post.assert_called_once_with(
        f'{os.getenv("NGINX")}/customers/sync',
        json={
            'id': str(mock_customer_instance.id),
            'firstName': valid_data['firstName'],
            'lastName': valid_data['lastName'],
            'phoneNumber': valid_data['phoneNumber'],
            'address': valid_data['address'],
            'country': valid_data['country'],
            'email': valid_data['email']
        }
    )

@patch('authentications_management.src.commands.create_customer.Customers')
@patch('authentications_management.src.commands.create_customer.db_session')
@patch('authentications_management.src.commands.create_customer.requests.post')
def test_create_customer_sync_service_failure(mock_requests_post, mock_db_session, mock_customers, valid_data):
    mock_customers.query.filter_by.return_value.first.return_value = None
    mock_customer_instance = MagicMock()
    mock_customer_instance.id = 1
    mock_customers.return_value = mock_customer_instance

    mock_requests_post.return_value.status_code = 500
    mock_requests_post.return_value.text = "Internal Server Error"

    command = CreateCustomer(valid_data)
    with pytest.raises(Exception, match="Failed to sync with customers service: Internal Server Error"):
        command.execute()

    mock_db_session.rollback.assert_called_once()

@patch('authentications_management.src.commands.create_customer.Customers')
@patch('authentications_management.src.commands.create_customer.db_session')
def test_create_customer_missing_nginx_env(mock_db_session, mock_customers, valid_data):
    mock_customers.query.filter_by.return_value.first.return_value = None
    mock_customer_instance = MagicMock()
    mock_customer_instance.id = 1
    mock_customers.return_value = mock_customer_instance

    os.environ.pop("NGINX", None)  # Ensure NGINX environment variable is not set

    command = CreateCustomer(valid_data)
    with pytest.raises(Exception, match="Invalid URL 'None/customers/sync': No scheme supplied."):
        command.execute()

    mock_db_session.rollback.assert_called_once()
    result = command.execute()

    assert result == {'message': 'Customer created successfully', 'customer_id': 1}
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()

@pytest.mark.parametrize("missing_field", ['firstName', 'lastName', 'country', 'address', 'phoneNumber', 'email'])
def test_missing_required_field(valid_data, missing_field):
    del valid_data[missing_field]
    command = CreateCustomer(valid_data)
    with pytest.raises(InvalidData):
        command.execute()

def test_invalid_address(valid_data):
    valid_data['address'] = '@@!!'
    command = CreateCustomer(valid_data)
    with pytest.raises(InvalidAddressCustomer):
        command.execute()

def test_invalid_phone(valid_data):
    valid_data['phoneNumber'] = '123456'
    command = CreateCustomer(valid_data)
    with pytest.raises(InvalidTelephoneCustomer):
        command.execute()

def test_invalid_email(valid_data):
    valid_data['email'] = 'invalid_email'
    command = CreateCustomer(valid_data)
    with pytest.raises(EmailDoesNotValid):
        command.execute()

@patch('authentications_management.src.commands.create_customer.Customers')
def test_user_already_exists(mock_customers, valid_data):
    mock_customers.query.filter_by.return_value.first.return_value = True
    command = CreateCustomer(valid_data)
    with pytest.raises(UserAlreadyExists):
        command.execute()