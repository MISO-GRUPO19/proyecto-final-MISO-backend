import datetime
from ..models.orders import Orders, OrderStatusHistory
from ..errors.errors import InvalidData
from ..models.database import db_session

class UpdateStateOrder:
    VALID_STATES = ['PENDIENTE', 'ENPORCESO', 'ENTREGADO', 'CANCELADO']

    def __init__(self, token, order_id, new_state):
        self.token = token
        self.order_id = order_id
        self.new_state = new_state

    def execute(self):
        if self.new_state not in self.VALID_STATES:
            raise InvalidData

        with db_session() as session:
            order = session.query(Orders).filter(Orders.id == self.order_id).first()
            
            if not order:
                raise InvalidData("Order not found")
        

            order.state = self.new_state
            
            order.status_history.append(
                OrderStatusHistory(
                    order_id=order.id,
                    state=self.new_state,
                    timestamp=datetime.datetime.now(
                        tz=datetime.timezone.utc)
                )
            )
            try:
                session.commit()
            except Exception as e:
                raise Exception("Database error") from e

        return {"message": f"Order {self.order_id} updated to {self.new_state}"}