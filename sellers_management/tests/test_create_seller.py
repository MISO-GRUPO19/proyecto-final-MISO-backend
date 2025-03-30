import unittest
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from sellers_management.src.api.sellers import sellers
from sellers_management.src.models.database import db_session
from sellers_management.src.commands.create_sellers import CreateSellers
from sellers_management.src.errors.errors import InvalidData

class TestCreateSellers(unittest.TestCase):

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

   '''
    
    def test_create_seller(self):
        #Pendiente enviar token
        with self.client:
            response = self.client.post('/sellers', json={
                "identification": "1223467",
                "name": "Product Name",
                "country": "Colombia",
                "address": "Calle 1 # 1 -1",
                "telephone": "574949494",
                "email": "test@test.com"
            })
            print(response.json)
            self.assertEqual(response.status_code, 201)
        
    def test_ping(self):
        with self.client:
            response = self.client.get('/sellers/ping')
            self.assertEqual(response.status_code, 200)
            self.assertIn('pong', response.json['message'])