import pytest
from unittest.mock import patch, MagicMock
from ai_services.src.commands.create_routes import CreatRoute
from ai_services.src.errors.errors import InvalidDate, InvalidData
from datetime import datetime, date
import json

@pytest.fixture
def mock_data():
    return {
        "date": "17-05-2025"
    }

@pytest.fixture
def mock_token():
    return "mock-token"

@pytest.fixture
def mock_orders_response():
    return [
        {"client_id": "cust1", "order_code": "ORD123"},
        {"client_id": "cust2", "order_code": "ORD456"}
    ]

@pytest.fixture
def mock_customer_response():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "address": "123 Main St"
    }

def test_validate_date_success(mock_data, mock_token):
    # Test with valid future date
    command = CreatRoute(mock_data, mock_token)
    
    # Mock datetime.now() to return a fixed date
    with patch('ai_services.src.commands.create_routes.datetime') as mock_datetime:
        mock_datetime.now.return_value = MagicMock(date=MagicMock(return_value=date(2025, 5, 1)))
        command.validate_date("17-05-2025")  # Should not raise exception

def test_validate_date_invalid_format(mock_data, mock_token):
    command = CreatRoute(mock_data, mock_token)
    
    with pytest.raises(InvalidDate, match="The provided date format is invalid"):
        command.validate_date("17/05/2025")  # Wrong format

def test_validate_date_past_date(mock_data, mock_token):
    command = CreatRoute(mock_data, mock_token)
    
    with patch('ai_services.src.commands.create_routes.datetime') as mock_datetime:
        mock_datetime.now.return_value = MagicMock(date=MagicMock(return_value=date(2025, 5, 20)))
        with pytest.raises(InvalidDate, match="cannot be in the past"):
            command.validate_date("17-05-2025")  # Date is before "today"

def test_execute_empty_date(mock_token):
    with pytest.raises(InvalidData):
        command = CreatRoute({"date": ""}, mock_token)
        command.execute()

@patch('ai_services.src.commands.create_routes.requests.get')
@patch('ai_services.src.commands.create_routes.db_session')
def test_execute_success(mock_db, mock_get, mock_data, mock_token, mock_orders_response, mock_customer_response):
    # Setup mock responses
    mock_get.side_effect = [
        MagicMock(status_code=200, json=MagicMock(return_value=mock_orders_response)),
        MagicMock(status_code=200, json=MagicMock(return_value=mock_customer_response)),
        MagicMock(status_code=200, json=MagicMock(return_value=mock_customer_response)),
    ]
    
    # Create command and execute
    command = CreatRoute(mock_data, mock_token)
    result = command.execute()
    
    # Verify results
    assert len(result) == 2
    assert result[0]["address"] == "123 Main St"
    assert mock_db.add.called
    assert mock_db.commit.called

@patch('ai_services.src.commands.create_routes.requests.get')
def test_get_orders_failure(mock_get, mock_data, mock_token):
    mock_get.return_value = MagicMock(status_code=400, text="Error message")
    
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(Exception, match="Error obtener al cliente"):
        command.get_orders_by_date()

@patch('ai_services.src.commands.create_routes.requests.get')
def test_get_customer_failure(mock_get, mock_data, mock_token):
    mock_get.return_value = MagicMock(status_code=400, text="Error message")
    
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(Exception, match="Error obtener al cliente"):
        command.get_customer_info("cust1")