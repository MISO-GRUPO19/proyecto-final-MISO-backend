from flask import jsonify
from .base_command import BaseCommand
from ..errors.errors import InvalidData, ProductInsufficientStock
from ..models.visits import Visits
from ..models.productOrder import ProductOrder
from ..models.database import db_session
from datetime import datetime
from ..models.orders import OrderStatusHistory
import os
from dotenv import load_dotenv 
from requests import Response
import requests
from datetime import datetime, timedelta
import random


load_dotenv()
AUTH = os.getenv("AUTHENTICATIONS")
CUSTOMERS = os.getenv("CUSTOMERS")

class GenerateSellerVisits(BaseCommand):

    def __init__(self, seller_id):
        self.seller_id = seller_id

    def execute(self):
        self.get_token()
        seller_json = self.get_seller_info()
        assigned_customers = seller_json['assigned_customers']
        visits = []
        for customer in assigned_customers:
            tomorrow = datetime.now() + timedelta(days=1)
            random_hour = random.randint(8, 18)  
            random_minute = random.randint(0, 59)  
            visit_date = tomorrow.replace(hour=random_hour, minute=random_minute, second=0, microsecond=0) 
            info = self.get_customer_info(customer)[0]
            visit = Visits(
                seller_id=self.seller_id,
                customer_id=info['id'],
                visit_date=visit_date,
                visit_address=info['address'],
                customer_name=f"{info['firstName']} {info['lastName']}",
                customer_phonenumber=info['phoneNumber'],
                store_name=f"{info['firstName']} {info['lastName']} Supermercado"
            )
            db_session.add(visit)
            db_session.commit()
            visits.append(visit)
        result = {
            "seller_id": self.seller_id,
            "visits_info": [
                {
                    "visit_id": each.id,
                    "visit_address": each.visit_address,
                    "customer_name": each.customer_name,
                    "customer_phonenumber": each.customer_phonenumber,
                    "store_name": each.store_name,
                    "visit_date": each.visit_date
                } for each in visits
            ]
        }
        return result



    def get_token(self):
        url = f'{AUTH}/users/login'
        payload = {
            "email": "admin@ccp.com",
            "password": "Admin123-"
        }
        response = requests.post(url, json=payload)
        response_json = response.json()
        self.token = response_json['access_token']
        
    def get_seller_info(self):
        url = f'{AUTH}/users/sellers/{self.seller_id}'
        headers = {
        'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error obteniendo al vendedor {response.text}")
        return response.json()

    def get_customer_info(self, customer_email):
        url = f'{CUSTOMERS}/customers/{customer_email}'
        headers = {
        'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error obtener al cliente {response.text}")
        return response.json()
