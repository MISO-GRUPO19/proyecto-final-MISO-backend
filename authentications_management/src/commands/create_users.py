import re
from .base_command import BaseCommand
from ..errors.errors import InvalidData, PasswordMismatch, UserAlreadyExists, EmailDoesNotValid, PasswordDoesNotHaveTheStructure
from ..models.users import Users
from ..models.database import db_session
from google.cloud import pubsub_v1
from ..pubsub.publisher import publish_message

class CreateUsers(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        required_fields = ['email', 'password', 'confirm_password', 'role']
        
        role_mapping = {
            1: 'Administrador',
            2: 'Vendedor',
            3: 'Cliente'
        }
        
        if self.data['role'] in role_mapping:
            self.data['role'] = role_mapping[self.data['role']]

        for field in required_fields:
            if field not in self.data or not self.data[field]:
                raise InvalidData

        if self.data['password'] != self.data['confirm_password']:
            raise PasswordMismatch

        if self.data['role'] not in ['Administrador', 'Vendedor', 'Cliente']:
            raise InvalidData

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, self.data['email']):
            raise EmailDoesNotValid

        password = self.data['password']
        if len(password) < 8:
            raise PasswordDoesNotHaveTheStructure
        if not re.search(r'[A-Z]', password):
            raise PasswordDoesNotHaveTheStructure
        if not re.search(r'[a-z]', password):
            raise PasswordDoesNotHaveTheStructure
        if not re.search(r'[0-9]', password):
            raise PasswordDoesNotHaveTheStructure
        if not re.search(r'[@$!%*?&]', password):
            raise PasswordDoesNotHaveTheStructure

        if Users.query.filter_by(email=self.data['email']).first():
            raise UserAlreadyExists

        publish_message('users', {
            'email': self.data['email'],
            'role': self.data['role'],
            'password': self.data['password']
        })

        return {'message': 'Usuario enviado a la cola exitosamente'}