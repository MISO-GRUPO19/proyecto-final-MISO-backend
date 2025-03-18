from .base_command import BaseCommand
from ..errors.errors import InvalidData
from ..models.manufacturers import Manufacturers
from ..models.database import db_session
from flask import jsonify

class CreateManufacturers(BaseCommand):
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        
        if (self.data['name'] == None or self.data['country'] == None or self.data['contact'] == None or self.data['telephone'] == None or self.data['email'] == None):
            raise InvalidData
        
        manufacturers = Manufacturers(
            name=self.data['name'],
            country=self.data['country'],
            contact=self.data['contact'],
            telephone=self.data['telephone'],
            email=self.data['email']
        )
        db_session.add(manufacturers)

        db_session.commit()
        db_session.close()

        return {'message': 'manufacturers created successfully'}