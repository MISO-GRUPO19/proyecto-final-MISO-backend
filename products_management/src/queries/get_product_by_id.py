from flask import jsonify
from commands.base_command import BaseCommand
from errors.errors import NotFound
from models.products import Products, ProductWarehouse
from models.batches import Batches

from models.database import db_session
from dotenv import load_dotenv 
import os
import requests
from requests import Response
from contextlib import contextmanager
from typing import Optional, Dict, List, Any, Union
import logging

# Carga las variables de entorno una sola vez
load_dotenv('../.env.development')
logging.basicConfig(level=logging.DEBUG)

MANUFACTURERS = os.getenv("MANUFACTURERS")


class GetById(BaseCommand):
    """Comando para obtener información de un producto por ID, nombre o código de barras."""

    @contextmanager
    def session_scope(self):
        """Proporciona un ámbito transaccional alrededor de una serie de operaciones."""
        session = db_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def __init__(self, identificator: str, token: str):
        self.identificator = identificator
        self.token = token
        
    def validate(self, session) -> None:
        """Valida que el producto exista en la base de datos."""
        if not session.query(Products).filter(
            (Products.barcode == self.identificator) | 
            (Products.name == self.identificator)
        ).first():
            raise NotFound

    def get_provider_name(self, provider_id: str) -> str:
        """Obtiene el nombre del proveedor desde el servicio externo."""
        headers = {"Authorization": f"Bearer {self.token}"}
        try:
            response: Response = requests.get(
                f'{MANUFACTURERS}/manufacturers/{provider_id}', 
                headers=headers,
                timeout=5
            )
            response.raise_for_status()
            return response.json()['name']
        except requests.exceptions.RequestException as e:
            raise Exception(f"Error al obtener proveedor: {str(e)}")

    def _get_product(self, session) -> Optional[Products]:
        """Intenta obtener el producto por barcode o nombre."""
        try:
            numerical_id = int(self.identificator)
            return session.query(Products).filter(
                Products.barcode == self.identificator
            ).first()
        except ValueError:
            return session.query(Products).filter(
                Products.name == self.identificator
            ).first()

    def _build_product_data(self, product: Products) -> Dict[str, Any]:
        """Construye los datos básicos del producto."""
        return {
            "product_name": product.name,
            "product_weight": product.weight,
            "product_provider_name": self.get_provider_name(product.provider_id),
            "product_price": product.price,
            "product_category": product.category
        }

    def _build_warehouse_data(self, product_warehouses: List[ProductWarehouse]) -> List[Dict[str, Any]]:
        """Construye los datos de almacén para el producto."""
        return [
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

    def execute(self) -> tuple:
        """Ejecuta el comando principal."""
        try:
            with self.session_scope() as session:
                self.validate(session)
                product = self._get_product(session)
                
                if not product:
                    raise NotFound
                
                product_warehouses = session.query(ProductWarehouse).filter(
                    ProductWarehouse.product_barcode == product.barcode
                ).all()
                
                response_data = {
                    "product_info": self._build_product_data(product),
                    "warehouse_info": self._build_warehouse_data(product_warehouses)
                }
                
                return jsonify(response_data), 200
                
        except NotFound:
            return jsonify({"error": "El producto no existe"}), 404
        except Exception as e:
            logging.error(f"Error interno: {str(e)}")
            return jsonify({"error": "Internal server error"}), 500