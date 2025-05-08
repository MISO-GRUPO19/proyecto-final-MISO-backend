from .base_command import BaseCommand
from ..errors.errors import *
from ..models.goals import GoalProduct, Goals
from ..models.database import db_session
from flask import jsonify
import re
import random
from datetime import datetime
import uuid
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PRODUCTS = os.getenv("PRODUCTS")
AUTH = os.getenv("AUTHENTICATIONS")


class CreateSellerGoals(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        required_fields = ["seller_id", "goals"]
        for field in required_fields:
            if field not in self.data:
                raise InvalidData(f"Missing required field: {field}")

        if not isinstance(self.data["goals"], list) or len(self.data["goals"]) == 0:
            raise InvalidData("The goals field must be a non-empty list")

        for goal in self.data["goals"]:
            if not isinstance(goal, dict):
                raise InvalidData("Each item in 'goals' must be a dictionary")
            if "product_barcode" not in goal or not goal["product_barcode"]:
                raise InvalidData("Each 'goal' must have a non-empty 'product_barcode' field")
            if "quantity" not in goal or not isinstance(goal["quantity"], int) or goal["quantity"] <= 0:
                raise InvalidData("Each 'goal' must have a positive integer 'quantity' field")
        now = datetime.now()
        formatted_date = now.strftime("%Y-%m-%d %H:%M:%S")
        self.get_token()

        try:
            for goal in self.data["goals"]:
                
                created_goal: Goals = Goals(
                    seller_id=self.data['seller_id'],
                    date=formatted_date
                )
                db_session.add(created_goal)
                db_session.commit()

                
                product_price = self.get_product_price(goal['product_barcode'])
                sales_expectation = round(product_price * goal['quantity'], 2)

                
                created_goal_product: GoalProduct = GoalProduct(
                    product_barcode=goal['product_barcode'],
                    quantity=goal['quantity'],
                    goal_id=created_goal.id,
                    date=formatted_date,
                    sales_expectation=sales_expectation
                )
                db_session.add(created_goal_product)
                db_session.commit()

            return {
                "message": "goals per product have been created successfully"
            }

        except Exception as e:
            db_session.rollback() 
            raise Exception(f"An error occurred while creating goals: {str(e)}")

        finally:
            db_session.close()
        
    def get_token(self):
        url = f'{AUTH}/users/login'
        payload = {
            "email": "admin@ccp.com",
            "password": "Admin123-"
        }
        response = requests.post(url, json=payload)
        response_json = response.json()
        self.token = response_json['access_token']

    def get_product_price(self, barcode):
        url = f'{PRODUCTS}/products/info/{barcode}'
        headers = {
            'Authorization': f'Bearer {self.token}'
        }
        response = requests.get(url, headers=headers)
        response_json = response.json()
        return response_json['product_info']['product_price']

