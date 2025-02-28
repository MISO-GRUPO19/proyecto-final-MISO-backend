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

        product = Products(name=self.name, description=self.description, price=self.price, category=self.category, weight=self.weight, useful_life=self.useful_life, provider_id=self.provider_id)
        db_session.add(product)

        db_session.commit()
        db_session.close()

        return {'message': 'Product created successfully'}