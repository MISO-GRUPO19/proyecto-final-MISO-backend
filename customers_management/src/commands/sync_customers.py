from ..models.stores import Stores
from ..models.customers import Customers
from ..models.database import db_session
import datetime

class SyncCustomer:
    def __init__(self, data):
        self.data = data

    def execute(self):
        session = db_session()
        try:
            customer = Customers(
                id=self.data['id'],
                firstName=self.data['firstName'],
                lastName=self.data['lastName'],
                phoneNumber=self.data['phoneNumber'],
                address=self.data['address'],
                country=self.data['country'],
                email=self.data['email'],
                seller_assigned=self.data['seller_id'],
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
            session.add(customer)
            
            store = Stores(
                customer_id=self.data['id'],
                address=self.data['address'],
                store_name=self.data['firstName'] + ' ' + self.data['lastName'] + ' Supermercado',
                created_at=datetime.datetime.utcnow(),
                updated_at=datetime.datetime.utcnow()
            )
            session.add(store)
            session.commit()
            return {'message': 'Customer synced successfully'}
        except Exception as e:
            session.rollback()
            return {'error': str(e)}
        finally:
            session.close()