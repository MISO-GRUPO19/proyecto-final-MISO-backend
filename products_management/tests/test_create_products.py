import pytest
from flask_testing import TestCase
from products_management.src.main import app, init_db
from products_management.src.models.database import db_session, base
from products_management.src.models.products import Products, Batch
from unittest.mock import patch

class TestCreateProducts(TestCase):
    def create_app(self):
        app.config.from_object('products_management.tests.conftest')
        return app

    def setUp(self):
        init_db()
        base.metadata.create_all(bind=db_session.bind)

    def tearDown(self):
        db_session.remove()
        base.metadata.drop_all(bind=db_session.bind)

    def test_create_product(self):
        response = self.client.post('/products', json={
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 19.99,
            'category': 'Category',
            'weight': 1.5,
            'barcode': '1234567890123',
            'provider_id': '123e4567-e89b-12d3-a456-426614174000',
            'batch': 'Batch001',
            'best_before': '2025-12-31T23:59:59',
            'quantity': 100
        })
        self.assertEqual(response.status_code, 201)
        self.assertIn('Producto creado exitosamente', response.json['message'])

        product = db_session.query(Products).filter_by(name='Product Name').first()
        self.assertIsNotNone(product)
        
        batch = db_session.query(Batch).filter_by(product_id=product.id).first()
        self.assertIsNotNone(batch)
        self.assertEqual(batch.quantity, 100)

    def test_create_product_invalid_name(self):
        response = self.client.post('/products', json={
            'name': '',
            'description': 'Product Description',
            'price': 19.99,
            'category': 'Category',
            'weight': 1.5,
            'barcode': '1234567890123',
            'provider_id': '123e4567-e89b-12d3-a456-426614174000',
            'batch': 'Batch001',
            'best_before': '2025-12-31T23:59:59',
            'quantity': 100
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Campos faltantes', response.json['message'])

    def test_create_product_invalid_provider_id(self):
        response = self.client.post('/products', json={
            'name': 'Valid Name',
            'description': 'Product Description',
            'price': 19.99,
            'category': 'Category',
            'weight': 1.5,
            'barcode': '1234567890123',
            'provider_id': 'INVALID-UUID',
            'batch': 'Batch001',
            'best_before': '2025-12-31T23:59:59',
            'quantity': 100
        })
        self.assertEqual(response.status_code, 400)
        self.assertIn('Error en los datos', response.json['message'])

    @pytest.mark.parametrize("field, value", [
        ('price', 'not-a-number'),
        ('quantity', 'invalid-int'),
        ('best_before', 'invalid-date')
    ])
    def test_create_product_invalid_types(self, field, value):
        data = {
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 19.99,
            'category': 'Category',
            'weight': 1.5,
            'barcode': '1234567890123',
            'provider_id': '123e4567-e89b-12d3-a456-426614174000',
            'batch': 'Batch001',
            'best_before': '2025-12-31T23:59:59',
            'quantity': 100
        }
        data[field] = value

        response = self.client.post('/products', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Error en los datos', response.json['message'])

    def test_create_product_missing_field(self):
        data = {
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 19.99,
            'category': 'Category',
            'weight': 1.5,
            'barcode': '1234567890123',
            'provider_id': '123e4567-e89b-12d3-a456-426614174000',
            'best_before': '2025-12-31T23:59:59',
            'quantity': 100
        }

        response = self.client.post('/products', json=data)
        self.assertEqual(response.status_code, 400)
        self.assertIn('Campos faltantes', response.json['message'])

    @patch('products_management.src.models.database.db_session.add')
    def test_create_product_db_error(self, mock_db_add):
        mock_db_add.side_effect = Exception("Database error")

        response = self.client.post('/products', json={
            'name': 'Product Name',
            'description': 'Product Description',
            'price': 19.99,
            'category': 'Category',
            'weight': 1.5,
            'barcode': '1234567890123',
            'provider_id': '123e4567-e89b-12d3-a456-426614174000',
            'batch': 'Batch001',
            'best_before': '2025-12-31T23:59:59',
            'quantity': 100
        })
        self.assertEqual(response.status_code, 500)
        self.assertIn('Database error', str(response.json))

    def test_ping(self):
        response = self.client.get('/products/ping')
        self.assertEqual(response.status_code, 200)
        self.assertIn('pong', response.json['message'])
