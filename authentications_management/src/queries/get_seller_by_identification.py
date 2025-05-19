from ..models.sellers import Sellers
from ..models.database import db_session
from contextlib import contextmanager
from uuid import UUID
from ..errors.errors import SellerNotFound

class GetSellerByIdentification():
    def __init__(self, identification):
        self.identification = identification
    
    def execute(self):
        if self.identification.isdigit():
            seller = db_session.query(Sellers).filter(Sellers.identification == self.identification).first()
        else:
        # Otherwise, treat it as a name
            seller = db_session.query(Sellers).filter(Sellers.name == self.identification).first()

        if not seller:
            raise SellerNotFound
        
        return {
            "id": str(seller.id),
            "name": seller.name,
            "country": seller.country,
            "phone": seller.telephone,
            "email": seller.email
        }