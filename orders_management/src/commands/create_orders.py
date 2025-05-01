from .base_command import BaseCommand
from ..errors.errors import InvalidData
from ..models.orders import Orders
from ..models.productOrder import ProductOrder
from ..models.database import db_session
from datetime import datetime
from ..models.orders import OrderStatusHistory
import os
from dotenv import load_dotenv 
from requests import Response
import requests

load_dotenv()

load_dotenv('../.env.development')

PRODUCTS = os.getenv("PRODUCTS")


class CreateOrders(BaseCommand):
    def __init__(self, token, client_id, seller_id, date, provider_id, total, order_type, route_id, products):
        self.token = token
        self.client_id = client_id
        self.seller_id = seller_id
        self.date = date
        self.provider_id = provider_id
        self.total = total
        self.order_type = order_type
        self.route_id = route_id
        self.products = products
    
    def validateProducts(self):
        for p in self.products:
            headers = {"Authorization": f"Bearer {self.token}"}
            response: Response = requests.get(f'{PRODUCTS}/products/{p["barcode"]}?quantity={p["quantity"]}', headers=headers)
            
            if response.status_code != 200:
                raise InvalidData            
                        
        

    def execute(self):
        if not all([self.client_id, self.date, self.total, self.order_type, self.products]):
            raise InvalidData
        
        self.validateProducts()
        
        try:
            order = Orders(
                client_id=self.client_id,
                seller_id=self.seller_id,
                date_order=datetime.fromisoformat(self.date),
                provider_id=self.provider_id,
                total=self.total,
                type=self.order_type,
                state='PENDIENTE',
                route_id=self.route_id
            )
            
            db_session.add(order)
            db_session.flush()

            initial_status = OrderStatusHistory(
                order_id=order.id,
                state=order.state,
                timestamp=datetime.utcnow()
            )
            db_session.add(initial_status)
            
            for p in self.products:
                product_order = ProductOrder(
                    product_barcode=p['barcode'],
                    order_id=order.id,
                    quantity=p['quantity']
                )
                db_session.add(product_order)
            
            db_session.commit()
            return {'message': 'Sale created successfully', 'id': order.id}
        
        except Exception as e:
            db_session.rollback()
            raise e
        
        finally:
            db_session.close()
