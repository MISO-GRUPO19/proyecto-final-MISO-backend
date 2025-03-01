from .base_command import BaseCommand
from ..errors.errors import InvalidData
from ..models.products import Products
from ..models.database import db_session
from flask import jsonify

class CreateProducts(BaseCommand):
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        
        if (self.data['name'] == '' or self.data['description'] == '' or self.data['price'] == '' or self.data['category'] == '' or self.data['weight'] == '' or self.data['useful_life'] == '' or self.data['provider_id'] == ''):
            raise InvalidData

        product = Products(name=self.data['name'], description=self.data['description'], price=self.data['price'], category=self.data['category'], weight=self.data['weight'], useful_life=self.data['useful_life'], provider_id=self.data['provider_id'])
        db_session.add(product)

        db_session.commit()
        db_session.close()

        return {'message': 'Product created successfully'}