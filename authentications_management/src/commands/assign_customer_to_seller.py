from .base_command import BaseCommand
from ..errors.errors import *
from ..models.sellers import Sellers
from flask import jsonify
import re
import random
from datetime import datetime
from ..models.database import db_session  

class AssignCustomerToSeller(BaseCommand):
    def __init__(self, data, seller_id):
        self.data = data
        self.seller_id = seller_id

    def execute(self):
        # Validate input
        if not self.data.get('customer_email'):
            raise InvalidData("Customer email is required")

        customer_email = self.data['customer_email']  
        seller_id_str = self.seller_id  

        # Get seller by seller_id
        seller = db_session.query(Sellers).filter(Sellers.id == seller_id_str).first()
        if not seller:
            raise SellerNotFound("Seller not found")

        # Initialize empty array if None
        if seller.assigned_customers is None:
            seller.assigned_customers = []

        # Append new customer ID if not already present
        if customer_email not in seller.assigned_customers:
            seller.assigned_customers = seller.assigned_customers + [customer_email]

        try:
            db_session.commit()
            return {
                'message': 'Customer has been successfully assigned to Seller',
                'seller_id': seller.id,
                'customer_email': customer_email
            }
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        finally:
            db_session.close()