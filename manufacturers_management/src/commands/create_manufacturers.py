from .base_command import BaseCommand
from ..errors.errors import *
from ..models.manufacturers import Manufacturers
from ..models.database import db_session
from flask import jsonify
import re

ALLOWED_COUNTRIES = [
    "Argentina", "Chile", "Brasil", "Ecuador", "Colombia"
]
class CreateManufacturers(BaseCommand):
    
    def __init__(self, data):
        self.data = data
    
    def execute(self):
        
        if (self.data['name'] == '' or self.data['country'] == '' or self.data['contact'] == '' or self.data['telephone'] == '' or self.data['email'] == ''):
            raise InvalidData
        
        if not self.check_name(self.data['name']):
            raise InvalidName
        
        if not self.check_country(self.data['country']):
            raise InvalidCountry
        
        if not self.check_contact(self.data['contact']):
            raise InvalidContact
        
        if not self.check_telephone(self.data['telephone']):
            raise InvalidTelephone
        
        if not self.check_email(self.data['email']):
            raise InvalidEmail

        manufacturers = Manufacturers(
            name=self.data['name'],
            country=self.data['country'],
            contact=self.data['contact'],
            telephone=self.data['telephone'],
            email=self.data['email']
        )
        db_session.add(manufacturers)

        db_session.commit()
        manufacturer_id = str(manufacturers.id)
        db_session.remove()

        return {
            'id': manufacturer_id,
            'message': 'manufacturers created successfully'
            }

    def check_name(self, name: str):
        if len(name) < 3 or len(name) > 100:
            return False
        if not re.match(r'^[\w\s\-.áéíóúÁÉÍÓÚñÑ]+$', name, re.UNICODE):
            return False
        existing_manufacturer = db_session.query(Manufacturers).filter_by(name=name).first()
        if existing_manufacturer:
            raise ExistingManufacturer
        return True

    def check_country(self, country: str):
        return country in ALLOWED_COUNTRIES
    
    def check_contact(self, contact: str):
        if len(contact) < 3 or len(contact) > 100:
            return False
        if not re.match(r'^[\w\s\-.áéíóúÁÉÍÓÚñÑ]+$', contact, re.UNICODE):
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