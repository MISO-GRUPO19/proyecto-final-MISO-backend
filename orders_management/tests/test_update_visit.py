import pytest
from unittest.mock import patch, MagicMock
from orders_management.src.commands.update_visit import UpdateVisit
from orders_management.src.errors.errors import InvalidData
from datetime import datetime, timedelta

@pytest.fixture
def mock_session():
    with patch('orders_management.src.commands.update_visit.db_session') as mock_db_session:
        yield mock_db_session


def test_execute_success(mock_session):
    visit_mock = MagicMock()
    visit_mock.id = "visit-uuid"
    session_mock = MagicMock()
    session_mock.query.return_value.filter.return_value.first.return_value = visit_mock
    mock_session.return_value.__enter__.return_value = session_mock

    service = UpdateVisit(token="abc123", visit_id="visit-uuid", new_state="VISITADO")

    response = service.execute()

    assert response == {"message": f"Visit {service.visit_id} updated to VISITADO"}
    assert visit_mock.visit_status == "VISITADO"
    assert isinstance(visit_mock.visit_date, datetime)
    now = datetime.now()
    assert now - visit_mock.visit_date < timedelta(seconds=5)

    session_mock.commit.assert_called_once()

def test_execute_invalid_state(mock_session):
    service = UpdateVisit(token="abc123", visit_id="visit-uuid", new_state="OTRO")

    with pytest.raises(InvalidData):
        service.execute()

def test_execute_visit_not_found(mock_session):
    session_mock = MagicMock()
    session_mock.query.return_value.filter.return_value.first.return_value = None
    mock_session.return_value.__enter__.return_value = session_mock

    service = UpdateVisit(token="abc123", visit_id="visit-uuid", new_state="NO_VISITADO")

    with pytest.raises(InvalidData, match="Visit not found"):
        service.execute()

def test_execute_commit_failure(mock_session):
    visit_mock = MagicMock()
    session_mock = MagicMock()
    session_mock.query.return_value.filter.return_value.first.return_value = visit_mock
    session_mock.commit.side_effect = Exception("DB error")
    mock_session.return_value.__enter__.return_value = session_mock

    service = UpdateVisit(token="abc123", visit_id="visit-uuid", new_state="VISITADO")

    with pytest.raises(Exception, match="Database error"):
        service.execute()
