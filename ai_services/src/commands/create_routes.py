from dotenv import load_dotenv
import re
import requests
from .base_command import BaseCommand
from ..errors.errors import InvalidData, InvalidDate
from ..models.routes import Routes
from ..models.database import db_session
import os
import random
import datetime
from datetime import datetime

load_dotenv()

load_dotenv('../.env.development')
ORDERS = os.getenv("ORDERS")
CUSTOMERS = os.getenv("CUSTOMERS")

class CreatRoute(BaseCommand):
    def __init__(self, data, token):
        self.data = data
        self.token = token
    
    def validate_date(self, date):
         try:
            delivery_date = datetime.strptime(date, "%d/%m/%Y").date()
            today = datetime.now().date()
            if delivery_date < today:
                raise InvalidDate("The provided date cannot be in the past.")
         except ValueError:
            raise InvalidDate("The provided date format is invalid. Use 'dd/MM/yyyy'.")


    def execute(self):
        if (self.data['date'] == ''):
            raise InvalidData
        
        normalized_date = self.data['date'].replace("-", "/")
        delivery_date = datetime.strptime(normalized_date, "%d/%m/%Y").date()
        self.validate_date(normalized_date)
        orders = self.get_orders_by_date()
        delivery_info = []
        delivery_aux = 1
        for order in orders:
            customer = self.get_customer_info(order['client_id'])
            delivery_info.append({
                "delivery": delivery_aux,
                "order_code": order['order_code'],
                "address": customer['address'],
                "customer_name": f"{customer['firstName']} {customer['lastName']}"
            })
            delivery_aux += 1
        
        
        sorted_list = sorted(delivery_info, key=lambda x: x['address'])
        route : Routes = Routes(
            delivery_date=delivery_date,
            delivery_information=sorted_list
        )
        db_session.add(route)
        db_session.commit()

        return sorted_list
        
    
    def get_orders_by_date(self):
        url = f'{ORDERS}/orders/date/{self.data["date"]}'
        headers = {
        'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error obtener al cliente {response.text}")
        return response.json()

    def get_customer_info(self, customer_id):
        url = f'{CUSTOMERS}/customers/{customer_id}'
        headers = {
        'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            raise Exception(f"Error obtener al cliente {response.text}")
        return response.json() 

