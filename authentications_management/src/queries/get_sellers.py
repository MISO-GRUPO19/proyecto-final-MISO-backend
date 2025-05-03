from ..models.sellers import Sellers
from ..models.database import db_session
from sqlalchemy import func

class GetSellers:
    def __init__(self, token):
        self.token = token

    def execute(self):
        try:
            sellers: Sellers = (
                db_session.query(
                    Sellers.id,
                    Sellers.identification,
                    Sellers.name
                )
                 .all()  
            )
            return [{"id": seller.id, "identification": seller.identification, "name": seller.name} for seller in sellers]
        except Exception as e:
            raise {'error': str(e)}
