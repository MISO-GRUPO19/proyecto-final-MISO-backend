from ..models.database import db_session
from ..models.orders import Orders
from datetime import datetime, timedelta
from sqlalchemy import func

class GetOrdersByDate:
    def __init__(self, date):
        self.date = date.replace("-", "/")
    
    def execute(self):
        try:
            target_date = datetime.strptime(self.date, "%d/%m/%Y").date() - timedelta(days=2)

            
            orders = db_session.query(Orders).filter(
                func.date(Orders.date_order) == target_date
            ).all()

            orders_list = []
            for order in orders:
                orders_list.append({
                    "order_id": order.id,
                    "order_code": order.code,
                    "client_id": order.client_id
                })
            
            return orders_list
        except Exception as e:
            return {'error': str(e)}
        finally:
            db_session.remove()


        