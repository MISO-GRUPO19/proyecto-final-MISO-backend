from .base_command import BaseCommand
from ..errors.errors import *
from ..models.sellers import Sellers
from flask import jsonify
import re
import random
from datetime import datetime
import uuid
from ..models.database import db_session  

class AssignCustomerToSeller(BaseCommand):
    def __init__(self, data, seller_id):
        self.data = data
        self.seller_id = seller_id

    def execute(self):
        # Validate input
        if not self.data.get('customer_id'):
            raise InvalidData("Customer ID is required")

        try:
            # Convert string UUID to UUID object
            customer_id = uuid.UUID(self.data['customer_id'])
            seller_id_uuid = uuid.UUID(self.seller_id)
        except (ValueError, AttributeError):
            raise InvalidData("Invalid UUID format")

        # Get seller with proper UUID conversion
        seller = db_session.query(Sellers).filter(Sellers.id == seller_id_uuid).first()
        if not seller:
            raise SellerNotFound("Seller not found")

        # Initialize empty array if None
        if seller.assigned_customers is None:
            seller.assigned_customers = []

        # Append new customer ID
        seller.assigned_customers = seller.assigned_customers + [customer_id]

        try:
            db_session.commit()
            return {
                'message': 'Customer has been successfully assigned to Seller',
                'seller_id': str(seller.id),
                'customer_id': str(customer_id)
            }
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        finally:
            db_session.close()