import pytest
from unittest.mock import patch, MagicMock
from orders_management.src.queries.get_orders_by_date import GetOrdersByDate
from datetime import datetime, date

@pytest.fixture
def mock_date():
    return "17-05-2025"

@pytest.fixture
def mock_orders():
    return [
        MagicMock(id="123e4567-e89b-12d3-a456-426614174000", code="ORCL12345678", client_id="456e7890-e12b-34d5-a678-426614174111"),
        MagicMock(id="123e4567-e89b-12d3-a456-426614174001", code="ORCL87654321", client_id="456e7890-e12b-34d5-a678-426614174112")
    ]

@patch("orders_management.src.queries.get_orders_by_date.db_session")
@patch("orders_management.src.queries.get_orders_by_date.Orders")
def test_execute(mock_orders_model, mock_db_session, mock_date, mock_orders):
    # Mock the query result
    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = mock_orders
    mock_db_session.query.return_value = mock_query

    # Create the GetOrdersByDate instance and execute
    query = GetOrdersByDate(mock_date)
    result = query.execute()

    # Assertions
    assert len(result) == 2
    assert result[0]["order_id"] == "123e4567-e89b-12d3-a456-426614174000"
    assert result[0]["order_code"] == "ORCL12345678"
    assert result[0]["client_id"] == "456e7890-e12b-34d5-a678-426614174111"
    assert result[1]["order_id"] == "123e4567-e89b-12d3-a456-426614174001"
    assert result[1]["order_code"] == "ORCL87654321"
    assert result[1]["client_id"] == "456e7890-e12b-34d5-a678-426614174112"

    # Ensure the query was called with the correct filter
    mock_query.filter.assert_called_once()

@patch("orders_management.src.queries.get_orders_by_date.db_session")
def test_execute_with_no_orders(mock_db_session, mock_date):
    # Mock the query result to return no orders
    mock_query = MagicMock()
    mock_query.filter.return_value.all.return_value = []
    mock_db_session.query.return_value = mock_query

    # Create the GetOrdersByDate instance and execute
    query = GetOrdersByDate(mock_date)
    result = query.execute()

    # Assertions
    assert len(result) == 0  # No orders should be returned

@patch("orders_management.src.queries.get_orders_by_date.db_session")
def test_execute_with_exception(mock_db_session, mock_date):
    # Mock the query to raise an exception
    mock_db_session.query.side_effect = Exception("Database error")

    # Create the GetOrdersByDate instance and execute
    query = GetOrdersByDate(mock_date)
    result = query.execute()

    # Assertions
    assert "error" in result
    assert result["error"] == "Database error"