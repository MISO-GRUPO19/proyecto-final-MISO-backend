import unittest
from flask import Flask, Response
from flask_jwt_extended import JWTManager, create_access_token
from manufacturers_management.src.api.manufacturers import manufacturers
from manufacturers_management.src.models.database import db_session
from manufacturers_management.src.commands.create_manufacturers import CreateManufacturers
from manufacturers_management.src.errors.errors import *

class TestCreateManufacturers(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'qwerty'  # Cambia esto por una clave secreta segura
        self.app.config['TESTING'] = True

        jwt = JWTManager(self.app)
        self.app.register_blueprint(manufacturers)

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
    
    def test_create_manufacturer(self):
        token = self.get_jwt_token()
        headers = {
            'Authorization': f'Bearer {token}'
        }
        with self.client:
            response = self.client.post('/manufacturers', json={
                "name": "Seller Pepito",
                "country": "Colombia",
                "contact": "Pepito Perez",
                "telephone": "574949494",
                "email": "test@test.com"
            }, headers=headers)
            self.assertEqual(response.status_code, 201)
    
    def test_create_manufacturer_invalid_data(self):
        data = {
                "name": "",
                "country": "Colombia",
                "contact": "Pepito Perez",
                "telephone": "574949494",
                "email": "test@test.com"
        }
        with self.assertRaises(InvalidData):  
            CreateManufacturers(data).execute()
    
    def test_create_manufacturer_invalid_name(self):
        data = {
                "name": "$%&&$%$&",
                "country": "Colombia",
                "contact": "Pepito Perez",
                "telephone": "574949494",
                "email": "test@test.com"
        }
        with self.assertRaises(InvalidName):  
            CreateManufacturers(data).execute()
    
    def test_create_manufacturer_invalid_country(self):
        data = {
                "name": "Fabricante a",
                "country": "Albaniax",
                "contact": "Pepito Perez",
                "telephone": "574949494",
                "email": "test@test.com"
        }
        with self.assertRaises(InvalidCountry):  
            CreateManufacturers(data).execute()
    
    def test_create_manufacturer_invalid_contact(self):
        data = {
                "name": "Fabricante A",
                "country": "Colombia",
                "contact": "?¡?&%&%",
                "telephone": "574949494",
                "email": "test@test.com"
        }
        with self.assertRaises(InvalidContact):  
            CreateManufacturers(data).execute()
    
    def test_create_manufacturer_invalid_telephone(self):
        data = {
                "name": "Fabricante A",
                "country": "Colombia",
                "contact": "Pepito Perez",
                "telephone": "hola",
                "email": "test@test.com"
        }
        with self.assertRaises(InvalidTelephone):  
            CreateManufacturers(data).execute()
    
    def test_create_manufacturer_invalid_email(self):
        data = {
                "name": "Fabricante a",
                "country": "Colombia",
                "contact": "Pepito Perez",
                "telephone": "574949494",
                "email": "testtest.com"
        }
        with self.assertRaises(InvalidEmail):  
            CreateManufacturers(data).execute()
    