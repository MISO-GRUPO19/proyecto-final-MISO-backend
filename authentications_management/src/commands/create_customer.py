import re
from .base_command import BaseCommand
from ..errors.errors import InvalidData, UserAlreadyExists, EmailDoesNotValid
from ..models.customers import Customers
from ..models.database import db_session

class CreateCustomer(BaseCommand):
    def __init__(self, data):
        self.data = data

    def execute(self):
        required_fields = ['name', 'country', 'address', 'telephone', 'email']
        for field in required_fields:
            if field not in self.data or not self.data[field]:
                raise InvalidData

        email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(email_regex, self.data['email']):
            raise EmailDoesNotValid

        if Customers.query.filter_by(email=self.data['email']).first():
            raise UserAlreadyExists

        try:
            customer = Customers(name=self.data['name'], country=self.data['country'], address=self.data['address'], telephone=self.data['telephone'], email=self.data['email'])
            db_session.add(customer)
            db_session.commit()
            return {'message': 'Cliente creado exitosamente'}
        except Exception as e:
            db_session.rollback()
            raise e
        finally:
            db_session.close()