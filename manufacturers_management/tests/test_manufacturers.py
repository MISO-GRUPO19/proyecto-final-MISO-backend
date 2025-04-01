import unittest
from unittest.mock import patch, MagicMock
from flask import Flask
from flask_jwt_extended import JWTManager, create_access_token
from manufacturers_management.src.api.manufacturers import manufacturers
from manufacturers_management.src.errors.errors import (
    InvalidData, InvalidName, InvalidCountry, InvalidContact, InvalidTelephone, InvalidEmail
)

class TestManufacturersAPI(unittest.TestCase):

    def setUp(self):
        self.app = Flask(__name__)
        self.app.config['JWT_SECRET_KEY'] = 'qwerty'
        self.app.config['JWT_TOKEN_LOCATION'] = ['headers']
        self.jwt = JWTManager(self.app)
        self.app.register_blueprint(manufacturers)
        self.client = self.app.test_client()
        self.access_token = create_access_token(identity="test_user")

    def auth_headers(self):
        return {'Authorization': f'Bearer {self.access_token}'}

    @patch('manufacturers_management.src.api.manufacturers.CreateManufacturers')
    def test_create_manufacturers_success(self, mock_create_manufacturers):
        mock_create_manufacturers.return_value.execute.return_value = {"message": "Manufacturer created successfully"}
        response = self.client.post('/manufacturers', json={"name": "Test Manufacturer", "country": "Colombia", "contact": "Test Contact", "telephone": "8765432123", "email": "email@ccp.com"}, headers=self.auth_headers())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json, {"message": "Manufacturer created successfully"})

    @patch('manufacturers_management.src.api.manufacturers.CreateManufacturers')
    def test_create_manufacturers_invalid_data(self, mock_create_manufacturers):
        mock_create_manufacturers.side_effect = InvalidData("Invalid data provided")
        response = self.client.post('/manufacturers', json={}, headers=self.auth_headers())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Invalid data"})

    @patch('manufacturers_management.src.api.manufacturers.GetManufacturerById')
    def test_get_manufacturer_by_id_success(self, mock_get_manufacturer_by_id):
        mock_get_manufacturer_by_id.return_value.execute.return_value = (
            {"name": "Test Manufacturer", "country": "USA"}, 200
        )
        response = self.client.get('/manufacturers/123e4567-e89b-12d3-a456-426614174000', headers=self.auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"name": "Test Manufacturer", "country": "USA"})

    @patch('manufacturers_management.src.api.manufacturers.GetManufacturer')
    def test_search_manufacturer_success(self, mock_get_manufacturer):
        mock_get_manufacturer.return_value.execute.return_value = (
            {"name": "Test Manufacturer", "country": "USA"}, 200
        )
        response = self.client.get('/manufacturers?name=Test Manufacturer', headers=self.auth_headers())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"name": "Test Manufacturer", "country": "USA"})

    def test_search_manufacturer_missing_name(self):
        response = self.client.get('/manufacturers', headers=self.auth_headers())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json, {"error": "Manufacturer name is required"})

    def test_ping(self):
        response = self.client.get('/manufacturers/ping')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"message": "pong"})
