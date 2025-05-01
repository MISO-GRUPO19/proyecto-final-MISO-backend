from typing import List, Dict, Any, Optional
from ..models.orders import Orders
from ..models.database import db_session
import requests
import os
from dotenv import load_dotenv
from requests import Response
from contextlib import contextmanager
from functools import lru_cache
from sqlalchemy.orm import joinedload

load_dotenv()
load_dotenv('../.env.development')

PRODUCTS = os.getenv("PRODUCTS")
AUTHENTICATIONS = os.getenv("AUTHENTICATIONS")

class GetOrderByClient:
    def __init__(self, token: str, client_id: str):
        self.client_id = client_id
        self.token = token
        self.session = requests.Session()
        self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    @contextmanager
    def _db_session(self):
        """Manejo seguro de sesiones de base de datos"""
        session = db_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    @lru_cache(maxsize=100)
    def _get_product_info(self, barcode: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de producto con cache"""
        try:
            response = self.session.get(f'{PRODUCTS}/products/{barcode}/warehouses', timeout=5)
            response.raise_for_status()
            return response.json().get('product_info')
        except requests.exceptions.RequestException:
            return None

    @lru_cache(maxsize=100)
    def _get_seller_info(self, seller_id: str) -> Optional[Dict[str, Any]]:
        """Obtiene información de vendedor con cache"""
        try:
            response = self.session.get(f'{AUTHENTICATIONS}/users/sellers/{seller_id}', timeout=5)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException:
            return None

    def _build_order_response(self, order: Orders) -> Dict[str, Any]:
        """Construye la respuesta para una orden individual"""
        # Productos con llamadas en paralelo (mejorable con asyncio)
        products = [{
            'name': self._get_product_info(item.product_barcode).get('product_name'),
            'barcode': item.product_barcode,
            'quantity': item.quantity
        } for item in order.product_items]

        # Historial de estados
        status_history = [{
            'status': status.state.value,
            'timestamp': status.timestamp.isoformat()
        } for status in sorted(order.status_history, key=lambda s: s.timestamp)]

        if order.seller_id is not None:
            # Información del vendedor
            seller_info = self._get_seller_info(str(order.seller_id)) or {}
        
        return {
            'id': str(order.id),
            'code': order.code,
            'client_id': str(order.client_id),
            'seller_id': str(order.seller_id),
            'seller_info': {
                'name': seller_info.get('name'),
                'identification': seller_info.get('identification'),
                'country': seller_info.get('country'),
                'address': seller_info.get('address'),
                'telephone': seller_info.get('telephone'),
                'email': seller_info.get('email')
            } if order.seller_id is not None else None,
            'date_order': order.date_order.isoformat(),
            'provider_id': str(order.provider_id),
            'total': order.total,
            'type': order.type.value,
            'state': order.state.value,
            'route_id': str(order.route_id),
            'products': products,
            'status_history': status_history
        }

    def execute(self) -> List[Dict[str, Any]]:
        """Obtiene todas las órdenes de un cliente"""
        try:
            with self._db_session() as session:
                orders = session.query(Orders)\
                    .filter(Orders.client_id == self.client_id)\
                    .options(
                        joinedload(Orders.product_items),
                        joinedload(Orders.status_history)
                    )\
                    .all()

                return [self._build_order_response(order) for order in orders]
                
        except Exception as e:
            # Loggear el error adecuadamente
            return [{'error': 'Failed to retrieve orders', 'details': str(e)}]