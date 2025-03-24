import pytest
from flask_testing import TestCase
from products_management.src.main import app, init_db
from products_management.src.models.database import db_session, base
from products_management.tests.conftest import test_client

class TestCreateProducts(TestCase):
    def create_app(self):
        app.config.from_object('products_management.tests.conftest')
        return app

    def setUp(self):
        base.metadata.create_all(bind=db_session.bind)

    def tearDown(self):
        db_session.remove()
        base.metadata.drop_all(bind=db_session.bind)

    def test_create_product(self):
        with self.client:
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

    def test_create_product_invalid_data(self):
        with self.client:
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
            print(response.json)
            self.assertIn('Datos inválidos', response.json['mssg'])

    def test_ping(self):
        with self.client:
            response = self.client.get('/products/ping')
            self.assertEqual(response.status_code, 200)
            self.assertIn('pong', response.json['message'])