import re
from .base_command import BaseCommand
from ..errors.errors import InvalidData, UserAlreadyExists, EmailDoesNotValid
from ..models.customers import Customers
from ..models.database import db_session

class CreateCustomer(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        required_fields = ['firstName', 'lastName' 'country', 'address', 'phoneNumber', 'email']
        for field in required_fields:
            if field not in self.data or not self.data[field]:
                raise InvalidData

        for field in ['firstName', 'lastName']:
            if not (3 <= len(self.data[field]) <= 50):
                raise InvalidData

        address_regex = r'^[a-zA-Z0-9\s#\-/.,]{5,150}$'
        if not re.match(address_regex, self.data['address']):
            raise InvalidData
        
        phone_regex = r'^\+[1-9][0-9]{6,13}$'
        if not re.match(phone_regex, self.data['phoneNumber']):
            raise InvalidData
        
        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, self.data['email']):
            raise EmailDoesNotValid

        if Customers.query.filter_by(email=self.data['email']).first():
            raise UserAlreadyExists

        try:
            customer = Customers(firstName=self.data['firstName'],lastName=self.data['lastName'], country=self.data['country'], address=self.data['address'], phoneNumber=self.data['phoneNumber'], email=self.data['email'])
            
            db_session.add(customer)
            db_session.commit()
            return {'message': 'Customer created successfully', 'customer_id': customer.id}
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()