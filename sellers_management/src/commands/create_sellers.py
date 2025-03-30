from .base_command import BaseCommand
from ..errors.errors import *
from ..models.sellers import Sellers
from ..models.database import db_session
from flask import jsonify
import re

ALLOWED_COUNTRIES = [
    "Argentina", "Bolivia", "Brazil", "Canada", "Chile", "Colombia", "Costa Rica",
    "Cuba", "Dominican Republic", "Ecuador", "El Salvador", "Guatemala", "Haiti",
    "Honduras", "Jamaica", "Mexico", "Nicaragua", "Panama", "Paraguay", "Peru",
    "United States", "Uruguay", "Venezuela"
]
class CreateSellers(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        if (self.data['name'] == '' or self.data['country'] == '' or self.data['identification'] == '' or self.data['address'] == '' or self.data['telephone'] == '' or self.data['email'] == '' ):
            raise InvalidData
        
        if self.check_identification(self.data['identification']) == False:
            raise InvalidIdentification
        
        if self.check_name(self.data['name']) == False:
            raise InvalidName

        if not self.check_country(self.data['country']):
            raise InvalidCountry
        
        if not self.check_address(self.data['address']):
            raise InvalidAddress
        
        if not self.check_telephone(self.data['telephone']):
            raise InvalidTelephone


        if not self.check_email(self.data['email']):
            raise InvalidEmail

        seller = Sellers(
            identification=self.data['identification'],
            name=self.data['name'], 
            country=self.data['country'], 
            address=self.data['address'], 
            telephone=self.data['telephone'], 
            email=self.data['email']
        )
        db_session.add(seller)
        db_session.commit()
        

        return {'message': 'Seller has been created successfully'}
    
    def check_identification(self, identification: str):
        if len(identification) < 6 or len(identification) > 20:
            return False
        if not re.match(r'^[a-zA-Z0-9]+$', identification):
            return False
        return True
    def check_name(self, name: str):
        if len(name) < 3 or len(name) > 100:
            return False
        if not re.match(r'^[a-zA-Z\s]+$', name):
            return False
        return True
    def check_country(self, country: str):
        return country in ALLOWED_COUNTRIES
    def check_address(self, address: str):
        if len(address) < 10 or len(address) > 200:
            return False
        return True
    def check_telephone(self, telephone: str):
        if len(telephone) < 7 or len(telephone) > 15:
            return False
        if not re.match(r'^\d+$', telephone):
            return False
        return True
    def check_email(self, email:str):
        if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
            return False
        return True