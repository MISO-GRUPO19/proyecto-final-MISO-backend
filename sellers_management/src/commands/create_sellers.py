from .base_command import BaseCommand
from ..errors.errors import InvalidData
from ..models.sellers import Sellers
from ..models.database import db_session
from flask import jsonify

class CreateSellers(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        if (self.data['name'] == '' or self.data['country'] == '' or self.data['address'] == '' or self.data['telephone'] == '' or self.data['email'] == '' ):
            raise InvalidData
        
        seller = Sellers(
            name=self.data['name'], 
            country=self.data['country'], 
            address=self.data['address'], 
            telephone=self.data['telephone'], 
            email=self.data['email']
        )
        db_session.add(seller)
        db_session.commit()
        

        return {'message': f'Seller {seller.name} has been created successfully'}