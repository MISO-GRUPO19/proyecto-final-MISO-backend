from .base_command import BaseCommand
from ..errors.errors import *
from ..models.sellers import Sellers, GoalProduct, Goals
from ..models.database import db_session
from .create_users import CreateUsers
from flask import jsonify
import re
import random
from datetime import datetime
import uuid


ALLOWED_COUNTRIES = [
    "Argentina", "Chile", "Brasil", "Ecuador", "Colombia"
]
class CreateSellers(BaseCommand):
    def __init__(self, data):
        self.data = data

    ''' HU11 Reporte de ventas vendedores '''
    def create_fake_goal(self, seller: Sellers):
        
        date = datetime(random.randint(2010,2025),random.randint(1,4),1)
        goal = Goals(
            seller_id=seller.id,
            date=date
        )
        db_session.add(goal)
        db_session.commit()    
        return goal
    
    def create_fake_goal_products(self, goal_created: Goals):
        quantity = random.randint(20, 100)
        sales = round(quantity * round(random.uniform(10.0, 100.0),2)) #Cantidad de producto * precio de venta
        sales_expectation = round(quantity * round(random.uniform(10.0, 100.0),2)) #Cantidad de producto * precio de venta
        goal_product = GoalProduct(
            product_id=uuid.uuid4(),
            quantity=quantity,
            goal_id=goal_created.id,
            date=goal_created.date,
            sales=sales,
            sales_expectation=sales_expectation
        )
        db_session.add(goal_product)
        db_session.commit()


    ''' FIN HU11 REPORTE DE VENTAS VENDEDORES'''
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

        identification = self.data['identification']

        password: str = f'{identification}@Pass'
        data = {
            "email": self.data['email'],
            "password": password,
            "confirm_password": password,
            "role": "Vendedor"
        }

        user_seller = CreateUsers(data).execute()
        if user_seller['message'] == 'Usuario enviado a la cola exitosamente':
            db_session.add(seller)
            db_session.commit()
            '''INICIO MODIFICACIÓN REPORTE DE VENTAS VENDEDORES'''
            for i in range(random.randint(2, 3)):
                goal = self.create_fake_goal(seller)
                self.create_fake_goal_products(goal)

            return {'message': 'Seller has been created successfully'}
    
    def check_identification(self, identification: str):
        if len(identification) < 6 or len(identification) > 20:
            return False
        existing_seller = db_session.query(Sellers).filter_by(identification=identification).first()
        if existing_seller:
            raise ExistingSeller
        if not re.match(r'^[a-zA-Z0-9]+$', identification):
            return False
        return True
    def check_name(self, name: str):
        if len(name) < 3 or len(name) > 100:
            return False
        if not re.match(r'^[\w\s\-.áéíóúÁÉÍÓÚñÑ]+$', name, re.UNICODE):
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