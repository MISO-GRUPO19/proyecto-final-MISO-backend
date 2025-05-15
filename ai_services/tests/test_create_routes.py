import pytest
from unittest.mock import patch, MagicMock
from ai_services.src.commands.create_routes import CreatRoute
from ai_services.src.errors.errors import InvalidDate
from datetime import datetime, date

@pytest.fixture
def mock_data():
    return {
        "date": "17-05-2025"
    }

@pytest.fixture
def mock_token():
    return "mock-token"

@patch("ai_services.src.commands.create_routes.datetime")
def test_validate_date(mock_datetime, mock_data, mock_token):
    # Setup mock
    mock_datetime.now.return_value.date.return_value = date(2025, 5, 16)
    
    command = CreatRoute(mock_data, mock_token)
    command.validate_date("17-05-2025")  # Should not raise

def test_invalid_date_format(mock_data, mock_token):
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(InvalidDate):
        command.validate_date("17/05/2025")

@patch("ai_services.src.commands.create_routes.datetime")
def test_past_date(mock_datetime, mock_data, mock_token):
    mock_datetime.now.return_value.date.return_value = date(2025, 5, 16)
    
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(InvalidDate):
        command.validate_date("15-05-2025")