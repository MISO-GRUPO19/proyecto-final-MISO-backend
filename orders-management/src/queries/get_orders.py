from ..models.orders import Orders
from ..models.database import db_session

class GetOrders:
    def __init__(self, token):
        self.token = token

    def execute(self):
        try:

            orders = db_session.query(Orders).all()

            orders_list = []
            for order in orders:
                orders_list.append({
                    'id': str(order.id),
                    'client_id': str(order.client_id),
                    'seller_id': str(order.seller_id),
                    'date_order': order.date_order.isoformat(),
                    'provider_id': str(order.provider_id),
                    'total': order.total,
                    'type': order.type.value,
                    'state': order.state.value,
                    'route_id': str(order.route_id),
                    'products': order.products
                })

            return orders_list

        except Exception as e:
            return {'error': str(e)}