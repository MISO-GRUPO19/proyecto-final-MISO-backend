from flask import jsonify
from ..models.customers import Customers
from ..models.database import db_session

class GetCustomers:
    def __init__(self):
        pass
    def execute(self):
        with db_session() as session:
            customers = session.query(Customers).all()
            result = []
            for customer in customers:
                result.append({
                    'firstName': customer.firstName,
                    'lastName': customer.lastName,
                    'country': customer.country,
                    'address': customer.address,
                    'email': customer.email,
                    'phoneNumber': customer.phoneNumber
                })
            return jsonify(result), 200