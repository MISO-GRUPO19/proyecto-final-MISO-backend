from .base_command import BaseCommand
from ..errors.errors import InvalidData, SellerNotFound
from ..models.sellers import Sellers
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
        
        # Get seller by seller_id using filter_by as expected by tests
        seller = db_session.query(Sellers).filter_by(id=self.seller_id).first()
        if not seller:
            raise SellerNotFound("Seller not found")

        # Initialize empty array if None
        if seller.assigned_customers is None:
            seller.assigned_customers = []

        # Check if customer already exists
        if customer_email in seller.assigned_customers:
            return {
                'message': 'Customer already assigned to seller',
                'seller_id': str(seller.id),
                'customer_email': customer_email
            }

        # Append new customer email
        seller.assigned_customers.append(customer_email)

        try:
            db_session.commit()
            return {
                'message': 'Customer has been successfully assigned to Seller',
                'seller_id': str(seller.id),
                'customer_email': customer_email
            }
        except Exception as e:
            db_session.rollback()
            raise RuntimeError(f"Database error: {str(e)}")
        finally:
            db_session.close()