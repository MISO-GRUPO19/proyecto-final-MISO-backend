from flask import jsonify
from ..models.customers import Customers
from ..models.database import db_session

class GetCustomers:
    def __init__(self):
        pass

    def execute(self):
        try:
            with db_session() as session:
                customers = session.query(Customers).options(
                    db_session.joinedload(Customers.stores)
                ).all()
                
                if not customers:
                    return jsonify({"message": "No customers found"}), 200
                
                customers_data = [
                    {
                        'firstName': customer.firstName,
                        'lastName': customer.lastName,
                        'country': customer.country,
                        'address': customer.address,
                        'email': customer.email,
                        'phoneNumber': customer.phoneNumber,
                        'id': customer.id,
                        'stores': [
                            {
                                'store_name': store.store_name,
                                'store_address': store.address
                            } for store in customer.stores
                        ]
                    } for customer in customers
                ]
                
                return jsonify(customers_data), 200
                
        except Exception as e:
            return jsonify({"error": "Internal server error"}), 500