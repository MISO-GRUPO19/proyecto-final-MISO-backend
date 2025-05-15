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
    # Mock today's date
    mock_datetime.now.return_value = datetime(2025, 5, 16)

    # Create the command and validate the date
    command = CreatRoute(mock_data, mock_token)
    command.validate_date(mock_data["date"])  # Should not raise an exception

def test_invalid_date_format(mock_data, mock_token):
    # Provide an invalid date format
    mock_data["date"] = "17/05/2025"  # Wrong format

    # Create the command and validate the date
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(InvalidDate):
        command.validate_date(mock_data["date"])

@patch("ai_services.src.commands.create_routes.datetime")
def test_past_date(mock_datetime, mock_data, mock_token):
    # Provide a past date
    mock_data["date"] = "15-05-2025"

    # Mock today's date
    mock_datetime.now.return_value = datetime(2025, 5, 16)

    # Create the command and validate the date
    command = CreatRoute(mock_data, mock_token)
    with pytest.raises(InvalidDate):
        command.validate_date(mock_data["date"])