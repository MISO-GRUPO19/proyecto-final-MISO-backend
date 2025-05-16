import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime
import uuid

from orders_management.src.queries.get_seller_sales_by_id import GetSellerSalesById
from orders_management.src.models.goals import Goals, GoalProduct
from orders_management.src.errors.errors import GoalNotFound

# --- Escenario 1: Éxito ---

@patch('orders_management.src.queries.get_seller_sales_by_id.requests.get')
@patch('orders_management.src.queries.get_seller_sales_by_id.requests.post')
@patch('orders_management.src.queries.get_seller_sales_by_id.db_session')
def test_execute_success(mock_db_session, mock_post, mock_get):
    # Datos simulados
    seller_id = uuid.uuid4()
    barcode = "123456"
    goal_id = uuid.uuid4()

    # Mock de token de autenticación
    mock_post.return_value.json.return_value = {"access_token": "fake-token"}

    # Mock de get_seller_id y get_product_price
    mock_get.side_effect = [
        MagicMock(json=lambda: {
            "id": str(seller_id),
            "name": "Juan",
            "country": "Colombia",
            "phone": "1234567890",
            "email": "juan@example.com"
        }),
        MagicMock(json=lambda: {
            "product_info": {"product_price": 10.0}
        })
    ]

    # Mock de goals y goals_product
    goal = Goals(seller_id=seller_id, date=datetime(2024, 1, 1))
    goal.id = goal_id
    goal_product = GoalProduct(
        product_barcode=barcode,
        quantity=5,
        goal_id=goal_id,
        date=datetime(2024, 1, 1),
        sales_expectation=50.0
    )

    mock_db_session.query.return_value.filter.return_value.all.return_value = [goal]
    mock_db_session.query.return_value.filter.return_value.first.return_value = goal_product

    # Mock del método que calcula cantidad vendida
    with patch.object(GetSellerSalesById, 'get_total_quantity_by_barcode', return_value=5):
        service = GetSellerSalesById("123")
        result, status_code = service.execute()

    # Validación de resultado
    assert status_code == 200
    assert result["name"] == "Juan"
    assert result["total_sales"] == 50.0
    assert result["monthly_summary"][0]["goals_achieved"] == 100.0


# --- Escenario 2: No hay metas ---

@patch('orders_management.src.queries.get_seller_sales_by_id.requests.get')
@patch('orders_management.src.queries.get_seller_sales_by_id.requests.post')
@patch('orders_management.src.queries.get_seller_sales_by_id.db_session')
def test_execute_goal_not_found(mock_db_session, mock_post, mock_get):
    mock_post.return_value.json.return_value = {"access_token": "fake-token"}
    mock_get.return_value.json.return_value = {
        "id": str(uuid.uuid4()),
        "name": "Juan",
        "country": "Colombia",
        "phone": "1234567890",
        "email": "juan@example.com"
    }

    mock_db_session.query.return_value.filter.return_value.all.return_value = []

    service = GetSellerSalesById("123")

    with pytest.raises(GoalNotFound):
        service.execute()


# --- Escenario 3: Error inesperado (fallo en requests) ---

@patch('orders_management.src.queries.get_seller_sales_by_id.requests.get')
@patch('orders_management.src.queries.get_seller_sales_by_id.requests.post')
def test_execute_unexpected_exception(mock_post, mock_get):
    mock_post.side_effect = Exception("Error de conexión")

    service = GetSellerSalesById("123")

    with pytest.raises(Exception) as e:
        service.execute()
    assert "Error de conexión" in str(e.value)
