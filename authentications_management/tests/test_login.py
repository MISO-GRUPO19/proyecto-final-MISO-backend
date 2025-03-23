import pytest
from flask import Flask
from flask_testing import TestCase
from authentications_management.src.main import app, init_db
from authentications_management.src.models.database import db_session, base
from authentications_management.src.models.users import Users, Role

class TestLogin(TestCase):
    def create_app(self):
        app.config.from_object('authentications_management.tests.conftest')
        return app

    def setUp(self):
        base.metadata.create_all(bind=db_session.bind)
        user = Users(email='test@example.com', password='Test1234!', role=Role.Administrador)
        db_session.add(user)
        db_session.commit()

    def tearDown(self):
        db_session.remove()
        base.metadata.drop_all(bind=db_session.bind)

    def test_login_success(self):
        with self.client:
            response = self.client.post('/users/login', json={
                'email': 'test@example.com',
                'password': 'Test1234!'
            })
            self.assertEqual(response.status_code, 200)
            self.assertIn('access_token', response.json)
            self.assertIn('refresh_token', response.json)

    def test_login_invalid_password(self):
        with self.client:
            response = self.client.post('/users/login', json={
                'email': 'test@example.com',
                'password': 'WrongPassword!'
            })
            self.assertEqual(response.status_code, 401)
            self.assertIn('Contraseña inválida', response.json['mssg'])

    def test_login_user_not_found(self):
        with self.client:
            response = self.client.post('/users/login', json={
                'email': 'nonexistent@example.com',
                'password': 'Test1234!'
            })
            self.assertEqual(response.status_code, 404)
            self.assertIn('Usuario no encontrado', response.json['mssg'])