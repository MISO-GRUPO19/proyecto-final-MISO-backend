import pytest
from unittest.mock import patch, MagicMock
from authentications_management.src.commands.create_customer import CreateCustomer
from authentications_management.src.errors.errors import InvalidAddressCustomer, InvalidData, InvalidTelephoneCustomer, UserAlreadyExists, EmailDoesNotValid

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
def test_create_customer_invalid_data(mock_customers, valid_data):
    valid_data['email'] = ''  # Correo inválido
    command = CreateCustomer(valid_data)
    with pytest.raises(InvalidData):
        command.execute()

@patch('authentications_management.src.commands.create_customer.Customers')
def test_create_customer_db_error(mock_customers, valid_data):
    mock_customers.query.filter_by.return_value.first.return_value = None
    mock_customers.side_effect = Exception("DB Error")
    command = CreateCustomer(valid_data)
    with pytest.raises(Exception):
        command.execute()

@patch('authentications_management.src.commands.create_customer.Customers')
@patch('authentications_management.src.commands.create_customer.db_session')
@patch('authentications_management.src.commands.create_customer.Customers')
@patch('authentications_management.src.commands.create_customer.db_session')
@patch.dict(os.environ, {"NGINX": "http://mocked-nginx"})
@patch('authentications_management.src.commands.create_customer.requests.post')
def test_create_customer_success(mock_post, mock_db_session, mock_customers, valid_data):
    mock_customers.query.filter_by.return_value.first.return_value = None
    mock_customer_instance = MagicMock()
    mock_customer_instance.id = 1
    mock_customer_instance.firstName = valid_data['firstName']
    mock_customer_instance.lastName = valid_data['lastName']
    mock_customer_instance.phoneNumber = valid_data['phoneNumber']
    mock_customer_instance.address = valid_data['address']
    mock_customer_instance.country = valid_data['country']
    mock_customer_instance.email = valid_data['email']
    mock_customers.return_value = mock_customer_instance

    mock_post.return_value.status_code = 200

    command = CreateCustomer(valid_data)
    result = command.execute()

    assert result == {'message': 'Customer created successfully', 'customer_id': 1}
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    mock_post.assert_called_once()


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