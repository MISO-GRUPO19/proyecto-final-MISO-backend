from .base_command import BaseCommand
from ..errors.errors import InvalidData
from ..models.orders import Orders
from ..models.database import db_session
from flask import jsonify

class CreateOrders(BaseCommand):
    def __init__(self, client_id, seller_id, date, provider_id, total, order_type, route_id, products):
        self.client_id = client_id
        self.seller_id = seller_id
        self.date = date
        self.provider_id = provider_id
        self.total = total
        self.order_type = order_type
        self.route_id = route_id
        self.products = products
        
    def execute(self):

        if (self.client_id == "" or self.seller_id == "" or self.date == "" or self.provider_id == "" or self.total == "" or self.order_type == "" or self.route_id == "" or self.products == ""):
            raise InvalidData
        
        orders = Orders(client_id=self.client_id, seller_id=self.seller_id, date_order=self.date, provider_id=self.provider_id, total=self.total, type=self.order_type, state='PENDIENTE', route_id=self.route_id, products=self.products)
        db_session.add(orders)
        
        db_session.commit()
        db_session.close()
        
        return {'message': 'Sale created successfully'}
    