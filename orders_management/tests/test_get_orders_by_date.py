import pytest
from unittest.mock import patch, MagicMock
from ai_services.src.commands.create_routes import CreatRoute
from ai_services.src.models.routes import Routes
from ai_services.src.errors.errors import InvalidData, InvalidDate
from datetime import datetime

@pytest.fixture
def mock_data():
    return {
        "date": "17-05-2025"
    }

@pytest.fixture
def mock_token():
    return "mock-token"

@pytest.fixture
def mock_orders():
    return [
        {
            "client_id": "123e4567-e89b-12d3-a456-426614174000",
            "order_code": "ORCL12345678"
        },
        {
            "client_id": "123e4567-e89b-12d3-a456-426614174001",
            "order_code": "ORCL87654321"
        }
    ]

@pytest.fixture
def mock_customer():
    return {
        "firstName": "John",
        "lastName": "Doe",
        "address": "123 Main St"
    }

@patch("ai_services.src.commands.create_routes.db_session")
@patch("ai_services.src.commands.create_routes.requests.get")
def test_execute(mock_requests_get, mock_db_session, mock_data, mock_token, mock_orders, mock_customer):
    # Mock the API responses
    mock_requests_get.side_effect = [
        MagicMock(status_code=200, json=MagicMock(return_value=mock_orders)),  # get_orders_by_date
        MagicMock(status_code=200, json=MagicMock(return_value=mock_customer)),  # get_customer_info (1st call)
        MagicMock(status_code=200, json=MagicMock(return_value=mock_customer))   # get_customer_info (2nd call)
    ]

    # Mock the database session
    mock_db_session.add = MagicMock()
    mock_db_session.commit = MagicMock()

    # Create the command and execute it
    command = CreatRoute(mock_data, mock_token)
    result = command.execute()

    # Assertions
    assert len(result) == 2
    assert result[0]["order_code"] == "ORCL12345678"
    assert result[1]["order_code"] == "ORCL87654321"
    assert mock_db_session.add.called
    assert mock_db_session.commit.called

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

def test_past_date(mock_data, mock_token):
    # Provide a past date
    mock_data["date"] = "15-05-2025"

    # Mock today's date
    with patch("ai_services.src.commands.create_routes.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2025, 5, 16)

        # Create the command and validate the date
        command = CreatRoute(mock_data, mock_token)
        with pytest.raises(InvalidDate):
            command.validate_date(mock_data["date"])