import pytest
from unittest.mock import patch, MagicMock
from flask import jsonify
from faker import Faker

fake = Faker()

@patch('customers_management.src.queries.get_customers.db_session')
@patch('customers_management.src.queries.get_customers.Customers')
def test_get_customers_execute_success(mock_customers, mock_db_session):
    mock_store_1 = MagicMock()
    mock_store_1.store_name = fake.company()
    mock_store_1.address = fake.address()

    mock_store_2 = MagicMock()
    mock_store_2.store_name = fake.company()
    mock_store_2.address = fake.address()

    mock_customer = MagicMock()
    mock_customer.firstName = fake.first_name()
    mock_customer.lastName = fake.last_name()
    mock_customer.country = fake.country()
    mock_customer.address = fake.address()
    mock_customer.email = fake.email()
    mock_customer.phoneNumber = fake.phone_number()
    mock_customer.stores = [mock_store_1, mock_store_2]
    mock_customer.id = 1

    mock_session = MagicMock()
    mock_session.query.return_value.all.return_value = [mock_customer]
    mock_db_session.return_value.__enter__.return_value = mock_session

    from customers_management.src.queries.get_customers import GetCustomers
    response, status_code = GetCustomers().execute()

    assert status_code == 200
    assert response.get_json() == [
        {
            'firstName': mock_customer.firstName,
            'lastName': mock_customer.lastName,
            'country': mock_customer.country,
            'address': mock_customer.address,
            'email': mock_customer.email,
            'phoneNumber': mock_customer.phoneNumber,
            'id': mock_customer.id,
            'stores': [
                {
                    'store_name': mock_store_1.store_name,
                    'store_address': mock_store_1.address
                },
                {
                    'store_name': mock_store_2.store_name,
                    'store_address': mock_store_2.address
                }
            ]
        }
    ]
