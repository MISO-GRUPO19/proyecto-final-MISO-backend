from ..models.sellers import Sellers
from ..models.database import db_session

class GetSellersById:
    def __init__(self, seller_id):
        self.seller_id = seller_id

    def execute(self):
        try:
            seller = db_session.query(Sellers).filter(Sellers.id == self.seller_id).first()
            if not seller:
                return {"error": "Seller not found"}, 404

            return {
                "id": str(seller.id),
                "name": seller.name,
                "identification": seller.identification,
                "country": seller.country,
                "address": seller.address,
                "telephone": seller.telephone,
                "email": seller.email
            }
        except Exception as e:
            return {"error": str(e)}, 500
