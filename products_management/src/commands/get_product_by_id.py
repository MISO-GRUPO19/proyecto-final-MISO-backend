from flask import jsonify
from commands.base_command import BaseCommand
from errors.errors import *
from models.products import Products, ProductWarehouse, Warehouses, db
from dotenv import load_dotenv 
import os
import requests
from requests import Response

load_dotenv()

load_dotenv('../.env.development')

NGINX = os.getenv("NGINX")

class GetById(BaseCommand):

    def __init__(self, identificator, token):
        self.identificator = identificator
        self.token = token
        
    def validate(self):
        product_barcode : Products = Products.query.filter(Products.barcode==self.identificator).first()
        product_name : Products =  Products.query.filter(Products.name==self.identificator).first()

        if not product_barcode and not product_name:
            raise NotFound

    def get_provider_name(self, provider_id):
        headers = {"Authorization": f"Bearer {self.token}"}
        response: Response = requests.get(f'{NGINX}/manufacturers/{provider_id}', headers=headers)
        data = response.json()
        return data['name']
        

    def execute(self):
        try:
            self.validate()
        except NotFound:
            return jsonify({"error": f"{ERROR_MESSAGES['not_found']}"})
        try:
            #Verifica que si el parametro es el codigo de barras
            numerical_id = int(self.identificator)
            product: Products = Products.query.filter(Products.barcode==self.identificator).first()
        except:
            product: Products = Products.query.filter(Products.name==self.identificator).first()
        
        product_warehouses = ProductWarehouse.query.filter(ProductWarehouse.product_barcode == product.barcode).all()
        product_data = {
            "product_name": f"{product.name}",
            "product_weight": f"{product.weight}",
            "product_provider_name": f"{self.get_provider_name(product.provider_id)}",
            "product_price": f"{product.price}",
            "product_category": f"{product.category}"
        }
        product_warehouse_data = [
            {
                "warehouse_name": pw.warehouse_name,
                "warehouse_address": pw.warehouse_address,
                "quantity": pw.quantity,
                "shelf": pw.shelf,
                "aisle": pw.aisle,
                "level": pw.level
            }
            for pw in product_warehouses
        ]
        return jsonify({
            "product_info": product_data,
            "warehouse_info": product_warehouse_data
        }), 200
            


