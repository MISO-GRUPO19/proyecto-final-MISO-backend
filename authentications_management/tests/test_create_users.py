import pytest
from flask_testing import TestCase
from authentications_management.src.main import app, init_db
from authentications_management.src.models.database import db_session, base
from authentications_management.tests.conftest import test_client

class TestCreateUsers(TestCase):
    def create_app(self):
        app.config.from_object('authentications_management.tests.conftest')
        return app

    def setUp(self):
        base.metadata.create_all(bind=db_session.bind)

    def tearDown(self):
        db_session.remove()
        base.metadata.drop_all(bind=db_session.bind)

    def test_create_user(self):
        with self.client:
            response = self.client.post('/users', json={
                'email': 'test@example.com',
                'password': 'Test1234!',
                'confirm_password': 'Test1234!',
                'role': '1'
            })
            self.assertEqual(response.status_code, 201)
            self.assertIn('Usuario creado exitosamente', response.json['message'])

    def test_create_user_invalid_email(self):
        with self.client:
            response = self.client.post('/users', json={
                'email': 'invalid-email',
                'password': 'Test1234!',
                'confirm_password': 'Test1234!',
                'role': 'CLIENTE'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos inválidos', response.json['mssg'])

    def test_create_user_password_mismatch(self):
        with self.client:
            response = self.client.post('/users', json={
                'email': 'test@example.com',
                'password': 'Test1234!',
                'confirm_password': 'Test12345!',
                'role': 'CLIENTE'
            })
            print(response.json)
            self.assertEqual(response.status_code, 400)
            self.assertIn('Confirmación de contraseña no coincide', response.json['mssg'])

    def test_create_user_invalid_role(self):
        with self.client:
            response = self.client.post('/users', json={
                'email': 'test@example.com',
                'password': 'Test1234!',
                'confirm_password': 'Test1234!',
                'role': 'INVALID_ROLE'
            })
            self.assertEqual(response.status_code, 400)
            self.assertIn('Datos inválidos', response.json['mssg'])
            
    def test_ping(self):
        with self.client:
            response = self.client.get('/users/ping')
            self.assertEqual(response.status_code, 200)
            self.assertIn('pong', response.json['message'])