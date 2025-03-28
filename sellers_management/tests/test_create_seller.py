import unittest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from sellers_management.src.api.sellers import sellers
from sellers_management.src.models.database import db_session
from sellers_management.src.commands.create_sellers import CreateProducts
from sellers_management.src.errors.errors import InvalidData

class TestCreateProducts(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'qwerty'  # Cambia esto por una clave secreta segura
        self.app.config['TESTING'] = True

        jwt = JWTManager(self.app)
        self.app.register_blueprint(sellers)

        self.client = self.app.test_client()

        with self.app.app_context():
            db_session.remove()

    def tearDown(self):
        with self.app.app_context():
            db_session.remove()

    '''
    def get_jwt_token(self):
        with self.app.app_context():
            access_token = create_access_token(identity='test_user')
            return access_token
    
    def test_create_product(self):
        token = self.get_jwt_token()
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with self.client:
            response = self.client.post('/products', json={
                'name': 'Product Name',
                'description': 'Product Description',
                'price': 19.99,
                'category': 'Electronics',
                'weight': 1.5,
                'barcode': '1234567890123',
                'provider_id': '123e4567-e89b-12d3-a456-426614174000',
                'batch': 'Batch001',
                'best_before': '2025-12-31T23:59:59',
                'quantity': 100
            }, headers=headers)
            print(response.json)
            self.assertEqual(response.status_code, 201)
            self.assertIn('Producto creado exitosamente', response.json['message'])

   '''
        
    def test_ping(self):
        with self.client:
            response = self.client.get('/products/ping')
            self.assertEqual(response.status_code, 200)
            self.assertIn('pong', response.json['message'])