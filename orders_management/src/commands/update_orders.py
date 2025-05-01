import datetime
from ..models.orders import Orders, OrderStatusHistory
from ..errors.errors import InvalidData
from ..models.database import db_session

class UpdateStateOrder:
    VALID_STATES = ['PENDIENTE', 'ENPORCESO', 'ENTREGADO', 'CANCELADO']

    def __init__(self, token, order_id: int, new_state: str):
        self.token = token
        self.order_id = order_id
        self.new_state = new_state

    def execute(self):
        if self.new_state not in self.VALID_STATES:
            raise InvalidData

        order = db_session.query(Orders).filter_by(id=self.order_id).first()
        if not order:
            raise InvalidData

        order.state = self.new_state
        
        order.status_history.append(
            OrderStatusHistory(
                order_id=order.id,
                state=self.new_state,
                timestamp=datetime.datetime.now(
                    tz=datetime.timezone.utc)
            )
        )
        db_session.commit()

        return {
            "message": "Order state updated successfully",
            "id": str(order.id)
        }
