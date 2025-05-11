from dotenv import load_dotenv
import re
import requests
from .base_command import BaseCommand
from ..errors.errors import InvalidAddressCustomer, InvalidData, InvalidNameCustomer, InvalidTelephoneCustomer, UserAlreadyExists, EmailDoesNotValid
from ..models.customers import Customers
from ..models.database import db_session
import os
import random

load_dotenv()

load_dotenv('../.env.development')

CUSTOMERS = os.getenv("CUSTOMERS")
AUTH = os.getenv("AUTHENTICATIONS")
class CreateCustomer(BaseCommand):
    def __init__(self, data):
        self.data = data
        

    def execute(self):
        self.get_token()
        required_fields = ['firstName', 'lastName', 'country', 'address', 'phoneNumber', 'email']
        for field in required_fields:
            if field not in self.data or not self.data[field]:
                raise InvalidData

        for field in ['firstName', 'lastName']:
            if not (3 <= len(self.data[field]) <= 50):
                raise InvalidNameCustomer

        address_regex = r'^[a-zA-Z0-9\s#\-/.,]{5,150}$'
        if not re.match(address_regex, self.data['address']):
            raise InvalidAddressCustomer
        
        phone_regex = r'^\+?[1-9][0-9]{6,13}$'
        if not re.match(phone_regex, self.data['phoneNumber']):
            raise InvalidTelephoneCustomer
        
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, self.data['email']):
            raise EmailDoesNotValid

        if Customers.query.filter_by(email=self.data['email']).first():
            raise UserAlreadyExists

        try:
            seller_id = self.assign_random_seller()
            customer = Customers(
                firstName=self.data['firstName'],
                lastName=self.data['lastName'],
                country=self.data['country'],
                address=self.data['address'],
                phoneNumber=self.data['phoneNumber'],
                email=self.data['email'],
                seller_assigned=seller_id
            )
            
            db_session.add(customer)
            db_session.commit()
            
            # Llamar al microservicio de clientes para sincronizar
            self.sync_with_customers_service(customer)
            self.update_seller_information(customer)
            return {'message': 'Customer created successfully', 'customer_id': customer.id}
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()

    def sync_with_customers_service(self, customer: Customers):
        url = f'{CUSTOMERS}/customers/sync'
        payload = {
            'id': str(customer.id),
            'firstName': customer.firstName,
            'lastName': customer.lastName,
            'phoneNumber': customer.phoneNumber,
            'address': customer.address,
            'country': customer.country,
            'email': customer.email,
            'seller_id': str(customer.seller_assigned)
        }
        response = requests.post(url, json=payload)
        if response.status_code != 200:
            raise Exception(f"Failed to sync with customers service: {response.text}")

    def get_token(self):
        url = f'{AUTH}/users/login'
        payload = {
            "email": "admin@ccp.com",
            "password": "Admin123-"
        }
        response = requests.post(url, json=payload)
        response_json = response.json()
        self.token = response_json['access_token']

    def assign_random_seller(self):
        url = f'{AUTH}/users/sellers'
        headers = {
        'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)  
        if response.status_code != 200:
            raise Exception(f"Error al traer los vendedores {response.text}")
        sellers = response.json()
        if sellers:
            assigned_seller = random.choice(sellers)
            return assigned_seller['id']
    
    def update_seller_information(self, customer: Customers):
        url = f'{AUTH}/users/sellers/{customer.seller_assigned}/customers'
        headers = {
        'Authorization': f'Bearer {self.token}'
        }
        payload = {
            'customer_email': f'{customer.email}'
        }
        response = requests.put(url, headers=headers, json=payload)
        if response.status_code != 200:
            raise Exception(f"Error al agregar cliente al vendedor {response.text}")
        
        
    