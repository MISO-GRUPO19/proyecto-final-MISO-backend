import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from products_management.src.api.products import products
from products_management.src.models.database import db_session
from products_management.src.queries.get_product_by_id import GetById
from products_management.src.errors.errors import InvalidData, NotFound

class TestGetProductById(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'qwerty'  # Cambia esto por una clave secreta segura
        self.app.config['TESTING'] = True

        jwt = JWTManager(self.app)
        self.app.register_blueprint(products)

        self.client = self.app.test_client()

        with self.app.app_context():
            db_session.remove()
    
    def tearDown(self):
        with self.app.app_context():
            db_session.remove()

    def get_jwt_token(self):
        with self.app.app_context():
            access_token = create_access_token(identity='test_user')
            return access_token
    @patch('requests.post')
    def test_get_product_by_barcode(self, mock_requests_post):
        token = self.get_jwt_token()
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with self.client:
            mock_requests_post.return_value.status_code = 201
            mock_requests_post.return_value.json.return_value = {"valid": True}
            response = self.client.get('/products/1234567890123/warehouses', 
                headers= headers
            )
            print(response.json)
            self.assertEqual(response.status_code, 200)
            self.assertGreater(len(response.json['warehouse_info']), 0)

