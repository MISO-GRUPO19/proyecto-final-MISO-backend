from ..models.stores import Stores
from ..models.customers import Customers
from ..models.database import db_session
import datetime

class SyncCustomer:
    def __init__(self, data):
        self.data = data

    def execute(self):
        try:
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
            
            store = Stores(
                customer_id=self.data['id'],
                address=self.data['address'],
                store_name=self.data['firstName'] + ' ' + self.data['lastName'] + ' Supermercado',
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
            db_session.add(store)
            db_session.commit()
            return {'message': 'Customer synced successfully'}
        except Exception as e:
            db_session.rollback()
            return {'error': str(e)}