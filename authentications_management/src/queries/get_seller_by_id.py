from ..models.sellers import Sellers
from ..models.database import db_session
from contextlib import contextmanager
from uuid import UUID

class GetSellersById:
    def __init__(self, seller_id):
        try:
            self.seller_id = UUID(seller_id) if not isinstance(seller_id, UUID) else seller_id
        except (ValueError, AttributeError):
            raise ValueError("Invalid seller ID format")

    @contextmanager
    def _session_scope(self):
        """Context manager para manejo automático de sesiones"""
        session = db_session()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()

    def execute(self):
        try:
            with self._session_scope() as session:
                seller = session.query(Sellers).filter(Sellers.id == self.seller_id).first()
                
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

        except ValueError as e:
            return {"error": str(e)}
        except Exception as e:
            return {"error": "Internal server error"}