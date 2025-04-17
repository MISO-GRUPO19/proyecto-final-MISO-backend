from ..models.orders import Orders
from ..models.database import db_session
import requests
import os
from dotenv import load_dotenv 
from requests import Response

load_dotenv()

load_dotenv('../.env.development')

NGINX = os.getenv("NGINX")

class GetOrderByClient:
    def __init__(self, token, client_id):
        self.client_id = client_id
        self.token = token

    def execute(self):
        try:
            orders = db_session.query(Orders).filter(Orders.client_id == self.client_id).all()

            orders_list = []
            for order in orders:
                # Productos
                products = []
                for item in order.product_items:
                    # Llamar al servicio para obtener los datos del producto
                    headers = {"Authorization": f"Bearer {self.token}"}
                    response = requests.get(f'{NGINX}/products/{item.product_barcode}/warehouses', headers=headers)
                    
                    if response.status_code == 200:
                        product_data = response.json()
                        product_info = product_data.get('product_info', {})
                        products.append({
                            'name': product_info.get('product_name'),
                            'barcode': item.product_barcode,
                            'quantity': item.quantity
                        })

                # Historial de estados
                status_history = []
                for status in sorted(order.status_history, key=lambda s: s.timestamp):
                    status_history.append({
                        'status': status.state.value,
                        'timestamp': status.timestamp.isoformat()
                    })

                # información del vendedor
                headers = {"Authorization": f"Bearer {self.token}"}
                response = requests.get(f'{NGINX}/users/sellers/{order.seller_id}', headers=headers)
                if response.status_code == 200:
                    seller_data = response.json()
                    seller_info = {
                        'name': seller_data.get('name'),
                        'identification': seller_data.get('identification'),
                        'country': seller_data.get('country'),
                        'address': seller_data.get('address'),
                        'telephone': seller_data.get('telephone'),
                        'email': seller_data.get('email')
                    }

                orders_list.append({
                    'id': str(order.id),
                    'code': order.code,
                    'client_id': str(order.client_id),
                    'seller_id': str(order.seller_id),
                    'seller_info': seller_info,
                    'date_order': order.date_order.isoformat(),
                    'provider_id': str(order.provider_id),
                    'total': order.total,
                    'type': order.type.value,
                    'state': order.state.value,
                    'route_id': str(order.route_id),
                    'products': products,
                    'status_history': status_history
                })

            return orders_list

        except Exception as e:
            return {'error': str(e)}