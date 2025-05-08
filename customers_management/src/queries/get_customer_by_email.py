from flask import jsonify
from ..models.customers import Customers
from ..models.database import db_session

class GetCustomerByEmail:
    def __init__(self, customer_email):
        self.customer_email = customer_email

    def execute(self):
        with db_session() as session:
            customers = session.query(Customers).filter(Customers.email == self.customer_email).all()
            if not customers:
                return jsonify({"error": "Customer not found"}), 404
            
            result = []
            for customer in customers:
                result.append({
                    'firstName': customer.firstName,
                    'lastName': customer.lastName,
                    'country': customer.country,
                    'address': customer.address,
                    'email': customer.email,
                    'phoneNumber': customer.phoneNumber,
                    'id': str(customer.id),
                    'stores': [
                        {
                            'store_name': store.store_name,
                            'store_address': store.address
                        } for store in customer.stores
                    ]
                })
            return jsonify(result), 200
