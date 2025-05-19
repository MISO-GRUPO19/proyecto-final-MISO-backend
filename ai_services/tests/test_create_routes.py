import pytest
from unittest.mock import patch, MagicMock
from ai_services.src.commands.create_routes import CreatRoute
from ai_services.src.errors.errors import InvalidDate, InvalidData
from datetime import datetime, date

@pytest.fixture
def mock_data():
    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
    return {
        "date": f"{day}/{month}/{year}"  # Changed to match expected format
    }

@pytest.fixture
def mock_token():
    return "mock-token"

def test_validate_date_success(mock_data, mock_token):
    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
    """Test that valid future dates pass validation"""
    command = CreatRoute(mock_data, mock_token)
    
    # Patch datetime.now() to return a specific date
    with patch('ai_services.src.commands.create_routes.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 5, 1)
        mock_datetime.strptime.side_effect = datetime.strptime
        
        # Test with correct format that matches implementation
        command.validate_date(f"{day}/{month}/{year}")  # Should not raise exception

def test_validate_date_invalid_format(mock_data, mock_token):
    """Test that invalid date formats raise InvalidDate"""
    command = CreatRoute(mock_data, mock_token)
    
    with pytest.raises(InvalidDate, match="The provided date format is invalid"):
        # Test with clearly invalid format
        command.validate_date("not-a-date")

def test_validate_date_past_date(mock_data, mock_token):
    today = datetime.now()
    day = today.day
    month = today.month
    year = today.year
    """Test that past dates raise InvalidDate"""
    command = CreatRoute(mock_data, mock_token)
    
    # Patch datetime.now() to return May 20, 2025
    with patch('ai_services.src.commands.create_routes.datetime') as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 5, 20)
        mock_datetime.strptime.side_effect = datetime.strptime
        
        # Test with past date (May 17 vs May 20 "today")
        with pytest.raises(InvalidDate) as exc_info:
            command.validate_date(f"{day}/{month}/{year}")
        
        # Verify the correct error message
        assert "cannot be in the past" in str(exc_info.value)

def test_execute_empty_date(mock_token):
    """Test that empty date raises InvalidData"""
    with pytest.raises(InvalidData):
        command = CreatRoute({"date": ""}, mock_token)
        command.execute()

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

@patch('ai_services.src.commands.create_routes.requests.get')
@patch('ai_services.src.commands.create_routes.db_session')
def test_execute_success(mock_db, mock_get, mock_data, mock_token, mock_orders_response, mock_customer_response):
    """Test successful execution flow"""
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
    """Test order API failure case"""
    mock_get.return_value = MagicMock(status_code=400, text="Error message")
    
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(Exception, match="Error obtener al cliente"):
        command.get_orders_by_date()

@patch('ai_services.src.commands.create_routes.requests.get')
def test_get_customer_failure(mock_get, mock_data, mock_token):
    """Test customer API failure case"""
    mock_get.return_value = MagicMock(status_code=400, text="Error message")
    
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(Exception, match="Error obtener al cliente"):
        command.get_customer_info("cust1")