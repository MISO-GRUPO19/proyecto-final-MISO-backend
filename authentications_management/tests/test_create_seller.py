import unittest
from flask import Flask, Response
from flask_jwt_extended import JWTManager, create_access_token
from authentications_management.src.api.users import users
from authentications_management.src.models.database import db_session
from authentications_management.src.commands.create_sellers import CreateSellers
from authentications_management.src.errors.errors import *
from unittest.mock import patch
from unittest.mock import MagicMock

class TestCreateSellers(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'qwerty'  # Cambia esto por una clave secreta segura
        self.app.config['TESTING'] = True

        jwt = JWTManager(self.app)
        self.app.register_blueprint(users)

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
        
    @patch('authentications_management.src.pubsub.publisher.pubsub_v1.PublisherClient')
    def test_create_seller(self, mock_publisher):
        mock_future = MagicMock()
        mock_future.result.return_value = "mocked-message-id"
        mock_publisher.return_value.publish.return_value = mock_future
        token = self.get_jwt_token()
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with self.client:
            response = self.client.post('/users/sellers', json={
                "identification": "1223467",
                "name": "Seller Pepito",
                "country": "Colombia",
                "address": "Calle 1 # 1 -1",
                "telephone": "574949494",
                "email": "test@test.com"
            }, headers=headers)
            self.assertEqual(response.status_code, 201)
    
    def test_create_seller_invalid_data(self):
        data = {
                "identification": "1223467",
                "name": "",
                "country": "Colombia",
                "address": "Calle 1 # 1 -1",
                "telephone": "574949494",
                "email": "test@test.com"
            }
        with self.assertRaises(InvalidData):  
            CreateSellers(data).execute()
    
    def test_create_seller_invalid_identification(self):
        data = {
                "identification": "eeee",
                "name": "Seller one",
                "country": "Colombia",
                "address": "Calle 1 # 1 -1",
                "telephone": "574949494",
                "email": "test@test.com"
            }
        with self.assertRaises(InvalidIdentification):  
            CreateSellers(data).execute()
    
    def test_create_seller_invalid_name(self):
        data = {
                "identification": "1223467",
                "name": "?¡#$%&%$",
                "country": "Colombia",
                "address": "Calle 1 # 1 -1",
                "telephone": "574949494",
                "email": "test@test.com"
            }
        with self.assertRaises(InvalidName):  
            CreateSellers(data).execute()
    
    def test_create_seller_invalid_country(self):
        data = {
                "identification": "1223467",
                "name": "seller one",
                "country": "Albaniax",
                "address": "Calle 1 # 1 -1",
                "telephone": "574949494",
                "email": "test@test.com"
            }
        with self.assertRaises(InvalidCountry):  
            CreateSellers(data).execute()
    
    def test_create_seller_invalid_address(self):
        data = {
                "identification": "1223467",
                "name": "seller",
                "country": "Colombia",
                "address": "Ca",
                "telephone": "574949494",
                "email": "test@test.com"
            }
        with self.assertRaises(InvalidAddress):  
            CreateSellers(data).execute()
    
    def test_create_seller_invalid_telephone(self):
        data = {
                "identification": "1223467",
                "name": "seller one",
                "country": "Colombia",
                "address": "Calle 1 # 1 -1",
                "telephone": "/())/%&%",
                "email": "test@test.com"
            }
        with self.assertRaises(InvalidTelephone):  
            CreateSellers(data).execute()
        
    def test_create_seller_invalid_email(self):
        data = {
                "identification": "1223467",
                "name": "seller one",
                "country": "Colombia",
                "address": "Calle 1 # 1 -1",
                "telephone": "574949494",
                "email": "testtest.com"
            }
        with self.assertRaises(InvalidEmail):  
            CreateSellers(data).execute()
