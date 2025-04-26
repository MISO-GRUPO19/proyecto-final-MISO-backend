from unittest.mock import patch
from authentications_management.src.models.database import init_db

@patch('authentications_management.src.models.database.db_session')
@patch('authentications_management.src.models.database.base.metadata.create_all')
def test_init_db(mock_create_all, mock_db_session):
    init_db()
    mock_create_all.assert_called_once()
    mock_db_session.commit.assert_called_once()