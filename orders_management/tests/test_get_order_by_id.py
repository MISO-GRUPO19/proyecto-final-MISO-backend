import pytest
import requests
from unittest.mock import MagicMock, patch, create_autospec
from typing import List, Dict, Any
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy.orm.query import Query
from faker import Faker
from orders_management.src.models.orders import Orders
from orders_management.src.queries.get_order_by_id import GetOrderById

fake = Faker()

class TestGetOrderById:
    
    @pytest.fixture(autouse=True)
    def setup_env(self, monkeypatch):
        monkeypatch.setenv('PRODUCTS', 'http://products-service')
        monkeypatch.setenv('AUTHENTICATIONS', 'http://auth-service')
        from importlib import reload
        import orders_management.src.queries.get_order_by_id
        reload(orders_management.src.queries.get_order_by_id)
        global GetOrderById
        from orders_management.src.queries.get_order_by_id import GetOrderById

    @pytest.fixture
    def mock_db_session(self):
        with patch('orders_management.src.queries.get_order_by_id.db_session') as mock:
            yield mock

    @pytest.fixture
    def mock_requests(self):
        with patch('orders_management.src.queries.get_order_by_id.requests.Session') as mock:
            yield mock

    @pytest.fixture
    def sample_order(self):
        order = MagicMock(spec=Orders)
        order.id = fake.uuid4()
        order.code = f"ORD-{fake.random_number(digits=5)}"
        order.client_id = fake.uuid4()
        order.seller_id = fake.uuid4()
        order.date_order = fake.date_time_this_year()
        order.provider_id = fake.uuid4()
        order.total = float(fake.random_number(digits=3))
        order.type = MagicMock(value=fake.random_element(elements=("standard", "express", "priority")))
        order.state = MagicMock(value=fake.random_element(elements=("pending", "processing", "shipped", "delivered")))
        order.route_id = fake.uuid4()
        
        product_items = []
        for _ in range(fake.random_int(min=1, max=5)):
            item = MagicMock()
            item.product_barcode = fake.ean13()
            item.quantity = fake.random_int(min=1, max=10)
            product_items.append(item)
        order.product_items = product_items
        
        status_history = []
        for i in range(fake.random_int(min=1, max=4)):
            status = MagicMock()
            status.state = MagicMock(value=fake.random_element(elements=("pending", "processing", "shipped", "delivered")))
            status.timestamp = order.date_order + timedelta(hours=i)
            status_history.append(status)
        order.status_history = status_history
        
        return order

    @pytest.fixture
    def sample_product_info(self):
        return {
            "product_info": {
                "product_name": fake.catch_phrase(),
                "description": fake.text(),
                "price": float(fake.random_number(digits=2)),
                "category": fake.word()
            }
        }

    @pytest.fixture
    def sample_seller_info(self):
        return {
            "name": fake.name(),
            "email": fake.email(),
            "identification": fake.random_number(digits=10),
            "country": fake.country(),
            "address": fake.address(),
            "telephone": fake.phone_number(),
            "company": fake.company()
        }

    def test_init(self):
        token = fake.uuid4()
        order_id = fake.uuid4()
        service = GetOrderById(token, order_id)
        assert service.token == token
        assert service.order_id == order_id

    def test_db_session_context_manager(self, mock_db_session):
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        
        mock_session_instance = MagicMock()
        mock_db_session.return_value = mock_session_instance
        
        with service._db_session() as session:
            mock_db_session.assert_called_once()
            assert session is mock_session_instance
        
        error_msg = fake.sentence()
        mock_session_instance.commit.side_effect = Exception(error_msg)
        with pytest.raises(Exception):
            with service._db_session():
                pass
        mock_session_instance.rollback.assert_called_once()
        mock_session_instance.close.assert_called()

    def test_get_product_info_success(self, mock_requests, sample_product_info):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_product_info
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_requests.return_value = mock_session
        
        barcode = fake.ean13()
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        result = service._get_product_info(barcode)
        
        assert result == sample_product_info["product_info"]
        mock_session.get.assert_called_with(f'http://products-service/products/{barcode}/warehouses', timeout=5)

    def test_get_product_info_failure(self, mock_requests):
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.RequestException(fake.sentence())
        mock_requests.return_value = mock_session
        
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        result = service._get_product_info(fake.ean13())
        
        assert result is None

    def test_get_seller_info_success(self, mock_requests, sample_seller_info):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_seller_info
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_requests.return_value = mock_session
        
        seller_id = fake.uuid4()
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        result = service._get_seller_info(seller_id)
        
        assert result == sample_seller_info
        mock_session.get.assert_called_with(f'http://auth-service/users/sellers/{seller_id}', timeout=5)

    def test_get_seller_info_failure(self, mock_requests):
        mock_session = MagicMock()
        mock_session.get.side_effect = requests.exceptions.RequestException(fake.sentence())
        mock_requests.return_value = mock_session
        
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        result = service._get_seller_info(fake.uuid4())
        
        assert result is None

    def test_build_order_response_success(self, mock_requests, sample_order, sample_product_info, sample_seller_info):
        mock_session = MagicMock()
        
        product_response = MagicMock()
        product_response.json.return_value = sample_product_info
        product_response.raise_for_status.return_value = None
        
        seller_response = MagicMock()
        seller_response.json.return_value = sample_seller_info
        seller_response.raise_for_status.return_value = None
        
        mock_session.get.side_effect = [product_response] * len(sample_order.product_items) + [seller_response]
        mock_requests.return_value = mock_session
        
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        result = service._build_order_response(sample_order)
        
        assert result['id'] == str(sample_order.id)
        assert result['products'][0]['name'] == sample_product_info["product_info"]["product_name"]
        assert result['seller_info']['name'] == sample_seller_info["name"]
        assert len(result['status_history']) == len(sample_order.status_history)

    def test_execute_success(self, mock_db_session, mock_requests, sample_order, sample_product_info, sample_seller_info):
        mock_session_instance = MagicMock()
        mock_db_session.return_value = mock_session_instance
        
        mock_query = MagicMock()
        mock_query.filter.return_value = mock_query
        mock_query.options.return_value = mock_query
        mock_query.all.return_value = [sample_order]
        mock_session_instance.query.return_value = mock_query
        
        mock_requests_session = MagicMock()
        product_response = MagicMock()
        product_response.json.return_value = sample_product_info
        seller_response = MagicMock()
        seller_response.json.return_value = sample_seller_info
        
        mock_requests_session.get.side_effect = [product_response] * len(sample_order.product_items) + [seller_response]
        mock_requests.return_value = mock_requests_session
        
        order_id = str(sample_order.id)
        service = GetOrderById(fake.uuid4(), order_id)
        result = service.execute()
        
        assert len(result) == 1
        assert result[0]['id'] == order_id
        mock_session_instance.commit.assert_called_once()
        mock_session_instance.close.assert_called_once()
        
        assert mock_query.filter.call_count == 1
        filter_args = mock_query.filter.call_args[0]
        assert len(filter_args) == 1
        

    def test_execute_db_error(self, mock_db_session):
        mock_session_instance = MagicMock()
        mock_db_session.return_value = mock_session_instance
        
        error_msg = "Error de base de datos"
        mock_session_instance.query.side_effect = Exception(error_msg)
        
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        result = service.execute()
        
        assert isinstance(result, list)
        assert len(result) == 1
        assert 'error' in result[0]
        assert 'details' in result[0]
        assert error_msg in result[0]['details']
        mock_session_instance.rollback.assert_called_once()
        mock_session_instance.close.assert_called_once()

    def test_lru_cache_behavior(self, mock_requests, sample_product_info):
        mock_session = MagicMock()
        mock_response = MagicMock()
        mock_response.json.return_value = sample_product_info
        mock_response.raise_for_status.return_value = None
        mock_session.get.return_value = mock_response
        mock_requests.return_value = mock_session
        
        service = GetOrderById(fake.uuid4(), fake.uuid4())
        barcode = fake.ean13()
        
        result1 = service._get_product_info(barcode)
        result2 = service._get_product_info(barcode)
        
        assert result1 == result2
        assert result1 == sample_product_info["product_info"]
        mock_session.get.assert_called_once()