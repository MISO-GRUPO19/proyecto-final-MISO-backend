from ..models.sellers import Sellers
from ..models.database import db_session

class GetSellers:
    def execute(self):
        try:
            
            sellers = db_session.query(Sellers).all()
            
            
            sellers_data = [
                {
                    "id": str(seller.id),
                    "name": seller.name,
                    "identification": seller.identification,
                    "email": seller.email,
                    "country": seller.country,
                    "address": seller.address,
                    "telephone": seller.telephone
                }
                for seller in sellers
            ]
            
            return sellers_data
        except Exception as e:
            raise Exception(f"Error fetching sellers: {str(e)}")