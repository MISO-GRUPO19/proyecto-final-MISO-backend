import unittest
from unittest.mock import patch, MagicMock
from orders_management.src.commands.update_orders import UpdateStateOrder
from orders_management.src.errors.errors import InvalidData
from orders_management.src.models.orders import Orders, OrderStatusHistory

class TestUpdateStateOrder(unittest.TestCase):

    def setUp(self):
        self.token = "test_token"
        self.order_id = "order123"
        self.valid_state = "ENTREGADO"
        self.invalid_state = "INVALIDO"

    @patch("orders_management.src.commands.update_orders.db_session")
    def test_execute_with_invalid_state_raises_exception(self, mock_db_session):
        use_case = UpdateStateOrder(self.token, self.order_id, self.invalid_state)

        with self.assertRaises(InvalidData):
            use_case.execute()
        mock_db_session.assert_not_called()

    @patch("orders_management.src.commands.update_orders.db_session")
    def test_execute_with_nonexistent_order_raises_exception(self, mock_db_session):
        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = None
        mock_db_session.return_value.__enter__.return_value = mock_session

        use_case = UpdateStateOrder(self.token, self.order_id, self.valid_state)

        with self.assertRaises(InvalidData) as context:
            use_case.execute()
        self.assertIn("Order not found", str(context.exception))

    @patch("orders_management.src.commands.update_orders.db_session")
    def test_execute_successful_update(self, mock_db_session):
        # Arrange
        mock_order = MagicMock(spec=Orders)
        mock_order.id = self.order_id
        mock_order.state = "PENDIENTE"
        mock_order.status_history = []

        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = mock_order
        mock_db_session.return_value.__enter__.return_value = mock_session

        use_case = UpdateStateOrder(self.token, self.order_id, self.valid_state)

        # Act
        result = use_case.execute()

        # Assert
        self.assertEqual(result, {"message": f"Order {self.order_id} updated to {self.valid_state}"})
        self.assertEqual(mock_order.state, self.valid_state)
        self.assertEqual(len(mock_order.status_history), 1)
        mock_session.commit.assert_called_once()

    @patch("orders_management.src.commands.update_orders.db_session")
    def test_execute_commit_fails_raises_exception(self, mock_db_session):
        mock_order = MagicMock(spec=Orders)
        mock_order.id = self.order_id
        mock_order.status_history = []

        mock_session = MagicMock()
        mock_session.query().filter().first.return_value = mock_order
        mock_session.commit.side_effect = Exception("DB failure")
        mock_db_session.return_value.__enter__.return_value = mock_session

        use_case = UpdateStateOrder(self.token, self.order_id, self.valid_state)

        with self.assertRaises(Exception) as context:
            use_case.execute()
        self.assertIn("Database error", str(context.exception))
