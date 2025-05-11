import pytest
from unittest.mock import patch, MagicMock
from authentications_management.src.commands.create_customer import CreateCustomer
from authentications_management.src.errors.errors import (
    InvalidAddressCustomer,
    InvalidData,
    InvalidNameCustomer,
    InvalidTelephoneCustomer,
    UserAlreadyExists,
    EmailDoesNotValid,
)
from authentications_management.src.models.customers import Customers
from authentications_management.src.models.database import db_session
import os


@pytest.fixture
def valid_data():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "country": "USA",
        "address": "123 Main St",
        "phoneNumber": "+12345678901",
        "email": "john.doe@example.com",
    }


@patch.dict(
    os.environ,
    {"CUSTOMERS": "http://mocked-customers", "AUTHENTICATIONS": "http://mocked-auth"},
)
@patch("authentications_management.src.commands.create_customer.requests.post")
@patch("authentications_management.src.commands.create_customer.requests.get")
@patch("authentications_management.src.commands.create_customer.requests.put")
@patch("authentications_management.src.commands.create_customer.db_session")
@patch("authentications_management.src.commands.create_customer.Customers")
def test_create_customer_success(
    mock_customers, mock_db_session, mock_put, mock_get, mock_post, valid_data
):
    # Mock token retrieval
    mock_post.side_effect = [
        MagicMock(status_code=200, json=MagicMock(return_value={"access_token": "mock-token"})),
        MagicMock(status_code=200),  # Sync with customers service
    ]

    # Mock seller retrieval
    mock_get.return_value.status_code = 200
    mock_get.return_value.json.return_value = [{"id": "seller-1"}]

    # Mock customer query
    mock_customers.query.filter_by.return_value.first.return_value = None

    # Mock customer instance
    mock_customer_instance = MagicMock()
    mock_customer_instance.id = 1
    mock_customer_instance.firstName = valid_data["firstName"]
    mock_customer_instance.lastName = valid_data["lastName"]
    mock_customer_instance.phoneNumber = valid_data["phoneNumber"]
    mock_customer_instance.address = valid_data["address"]
    mock_customer_instance.country = valid_data["country"]
    mock_customer_instance.email = valid_data["email"]
    mock_customer_instance.seller_assigned = "seller-1"
    mock_customers.return_value = mock_customer_instance

    # Execute the command
    command = CreateCustomer(valid_data)
    result = command.execute()

    # Assertions
    assert result == {"message": "Customer created successfully", "customer_id": 1}
    mock_db_session.add.assert_called_once()
    mock_db_session.commit.assert_called_once()
    assert mock_post.call_count == 2
    mock_get.assert_called_once()
    mock_put.assert_called_once()


@patch.dict(
    os.environ,
    {"CUSTOMERS": "http://mocked-customers", "AUTHENTICATIONS": "http://mocked-auth"},
)
def test_create_customer_invalid_email(valid_data):
    valid_data["email"] = "invalid-email"  # Invalid email format
    command = CreateCustomer(valid_data)
    with pytest.raises(EmailDoesNotValid):
        command.execute()


@patch.dict(
    os.environ,
    {"CUSTOMERS": "http://mocked-customers", "AUTHENTICATIONS": "http://mocked-auth"},
)
@patch("authentications_management.src.commands.create_customer.Customers")
def test_create_customer_user_already_exists(mock_customers, valid_data):
    # Mock existing customer
    mock_customers.query.filter_by.return_value.first.return_value = MagicMock()

    command = CreateCustomer(valid_data)
    with pytest.raises(UserAlreadyExists):
        command.execute()


@patch.dict(
    os.environ,
    {"CUSTOMERS": "http://mocked-customers", "AUTHENTICATIONS": "http://mocked-auth"},
)
def test_create_customer_missing_required_field(valid_data):
    del valid_data["firstName"]  # Remove a required field
    command = CreateCustomer(valid_data)
    with pytest.raises(InvalidData):
        command.execute()