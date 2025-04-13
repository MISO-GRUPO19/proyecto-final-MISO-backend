import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from products_management.src.api.products import products
from products_management.src.models.database import db_session
from products_management.src.queries.get_product_by_id import GetById
from products_management.src.errors.errors import InvalidData, NotFound
from types import SimpleNamespace

class TestGetProductById(unittest.TestCase):

    @patch('products_management.src.queries.get_products_by_id.db_session')
    def test_execute_returns_correct_product_warehouse(self, mock_db_session):
        mock_db_session.query().outerjoin().group_by().all.return_value = [
            SimpleNamespace(
                name="Producto A", 
                barcode="123ABC", 
                stock=10, 
                price=5.5,
                warehouse_info={
                    "name": "Bodega A",
                    "address": "123 Main St",
                    "quantity": 100,
                    "shelf": "A",
                    "aisle": "1",
                    "level": 1
                }
                )
        ]

        service = GetById("123ABC", token="dummy-token")
        result = service.execute()
        self.assertEqual(len(result), 1)
        self.assertEqual(result['product_info']['product_name'], "Producto A")
        self.assertEqual(result['warehouse_info']['warehouse_name'], "Bodega A")
        
        
