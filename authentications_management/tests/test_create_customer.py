import pytest
from unittest.mock import patch, MagicMock
from authentications_management.src.commands.create_customer import CreateCustomer
from authentications_management.src.errors.errors import InvalidData, UserAlreadyExists, EmailDoesNotValid

@pytest.fixture
def valid_data():
    return {
        'firstName': 'John',
        'lastName': 'Doe',
        'country': 'USA',
        'address': '123 Main St',
        'phoneNumber': '+12345678901',
        'email': 'john.doe@example.com'
    }

@patch('authentications_management.src.commands.create_customer.Customers')
@patch('authentications_management.src.commands.create_customer.db_session')
def test_create_customer_success(mock_db_session, mock_customers, valid_data):
    mock_customers.query.filter_by.return_value.first.return_value = None
    mock_customer_instance = MagicMock()
    mock_customer_instance.id = 1
    mock_customers.return_value = mock_customer_instance

    command = CreateCustomer(valid_data)
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
    with pytest.raises(InvalidData):
        command.execute()

def test_invalid_phone(valid_data):
    valid_data['phoneNumber'] = '123456'
    command = CreateCustomer(valid_data)
    with pytest.raises(InvalidData):
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