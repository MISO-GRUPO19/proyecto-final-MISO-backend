from ..models.customers import Customers
from ..models.database import db_session
import datetime

class SyncCustomer:
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
            customer = Customers.query.filter_by(id=self.data['id']).first()
            if customer:
                # Actualizar cliente existente
                customer.firstName = self.data['firstName']
                customer.lastName = self.data['lastName']
                customer.phoneNumber = self.data['phoneNumber']
                customer.address = self.data['address']
                customer.country = self.data['country']
                customer.email = self.data['email']
                customer.updated_at = datetime.datetime.utcnow()
            else:
                # Crear nuevo cliente
                customer = Customers(
                    id=self.data['id'],
                    firstName=self.data['firstName'],
                    lastName=self.data['lastName'],
                    phoneNumber=self.data['phoneNumber'],
                    address=self.data['address'],
                    country=self.data['country'],
                    email=self.data['email'],
                    created_at=datetime.datetime.utcnow(),
                    updated_at=datetime.datetime.utcnow()
                )
                db_session.add(customer)
            db_session.commit()
            return {'message': 'Customer synced successfully'}
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}