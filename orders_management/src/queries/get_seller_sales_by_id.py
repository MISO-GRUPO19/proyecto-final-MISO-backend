
from ..errors.errors import *
from ..models.goals import GoalProduct, Goals
from ..models.orders import *
from ..models.productOrder import *
from ..models.database import db_session
from flask import jsonify
import re
import random
from datetime import datetime
import uuid
import os
from sqlalchemy import extract, func, cast, String
from dotenv import load_dotenv
import requests

load_dotenv()

AUTH = os.getenv("AUTHENTICATIONS")
PRODUCTS = os.getenv("PRODUCTS")

class GetSellerSalesById():
    def __init__(self, seller_identification):
        self.seller_identification = seller_identification

    def execute(self):
        self.get_token()
        seller_info = self.get_seller_id()
        seller_id = seller_info['id']
        seller_name = seller_info['name']
        seller_country = seller_info['country']
        seller_phone = seller_info['phone']
        seller_email = seller_info['email']
        try:
            goals = db_session.query(Goals).filter(Goals.seller_id == seller_id).all()
            if not goals:
                raise GoalNotFound
            monthly_summary = []
            total_seller_sales = 0
            monthly_sales = 0
            monthly_expecation = 0
            sales = 0
            barcodes = []
            for goal in goals:    
                product_goal: GoalProduct = db_session.query(GoalProduct).filter(GoalProduct.goal_id == goal.id).first()
                monthly_expecation += product_goal.sales_expectation
                date = product_goal.date.strftime("%m-%Y")
                barcodes.append(product_goal.product_barcode)

            unique_barcodes = list(set(barcodes))
            ''' Sales calculation '''
            for barcode in unique_barcodes:
                product_price = self.get_product_price(barcode)
                product_total_quantity = self.get_total_quantity_by_barcode(seller_id, datetime.now().month, datetime.now().year, barcode)
                sales = round(product_price * product_total_quantity, 2) if product_total_quantity > 0 else 0
                total_seller_sales += sales
                monthly_sales += sales
            
            goals_achieved = round((monthly_sales / monthly_expecation) * 100, 2) if monthly_expecation > 0 else 0
            monthly_summary.append({
                    "date": date,  
                    "total_sales": round(monthly_sales,2),
                    "goals": round(monthly_expecation,2),
                    "goals_achieved": goals_achieved  
            })
                
            seller_data = {
                "name" : f"{seller_name}",
                "country": f"{seller_country}",
                "phone": f"{seller_phone}",
                "email": f"{seller_email}",
                "total_sales": round(total_seller_sales, 2),
                "monthly_summary": monthly_summary
            }
            
            return seller_data, 200
        except Exception as e:
            raise e
        
    def get_token(self):
        url = f'{AUTH}/users/login'
        payload = {
            "email": "admin@ccp.com",
            "password": "Admin123-"
        }
        response = requests.post(url, json=payload)
        response_json = response.json()
        self.token = response_json['access_token']

    def get_seller_id(self):
        url = f'{AUTH}/users/sellers/{self.seller_identification}'
        response = requests.get(url)
        response_json = response.json()
        return response_json

    def get_product_price(self, barcode):
        url = f'{PRODUCTS}/products/info/{barcode}'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)
        response_json = response.json()
        return response_json['product_info']['product_price']
 
    def get_total_quantity_by_barcode(self, seller_id, month, year, product_barcode):
        try:
            # Paso 1: Filtrar las órdenes por seller_id y fecha
            order_ids = db_session.query(Orders.id).filter(
                Orders.seller_id == seller_id,
                extract("month", Orders.date_order) == month,
                extract("year", Orders.date_order) == year
            ).subquery()  # Subquery para usar en el siguiente filtro

            # Paso 2: Filtrar las ProductOrder relacionadas con las órdenes y el barcode
            total_quantity = db_session.query(func.sum(ProductOrder.quantity)).filter(
                ProductOrder.order_id.in_(order_ids),
                ProductOrder.product_barcode == product_barcode
            ).scalar()  # Obtener el valor directamente

            # Si no hay resultados, retornar 0
            return total_quantity or 0
        except Exception as e:
            raise Exception(f"An error occurred while fetching total quantity: {str(e)}")



