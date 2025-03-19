from .base_command import BaseCommand
from ..errors.errors import InvalidData, PasswordMismatch
from ..models.users import Users
from ..models.database import db_session
from flask import jsonify

class CreateUsers(BaseCommand):
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        
        if (self.data['email'] == '' or self.data['password'] == '' or self.data['confirm_password'] == '' or self.data['role'] == ''):
            raise InvalidData

        if (self.data['password'] != self.data['confirm_password']):
            raise PasswordMismatch
        
        user = Users(email=self.data['email'], role=self.data['role'])
        user.set_password(self.data['password'])
        db_session.add(user)
        db_session.commit()
        db_session.close()
        return {'message': 'Usuario creado correctamente'}
