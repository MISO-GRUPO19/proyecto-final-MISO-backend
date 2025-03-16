from .base_command import BaseCommand
from ..errors.errors import InvalidData
from ..models.ai import AI
from ..models.database import db_session
from flask import jsonify

class CreateAI(BaseCommand):
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        
        if (self.data['name'] == '' or self.data['country'] == '' or self.data['contact'] == '' or self.data['telephone'] == '' or self.data['email'] == ''):
            raise InvalidData
        
        ai = AI(
            name=self.data['name'],
            country=self.data['country'],
            contact=self.data['contact'],
            telephone=self.data['telephone'],
            email=self.data['email']
        )
        db_session.add(ai)

        db_session.commit()
        db_session.close()

        return {'message': 'Customer created successfully'}