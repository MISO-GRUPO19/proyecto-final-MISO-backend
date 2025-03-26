import pytest
from dotenv import load_dotenv, find_dotenv
import os
import sys



# Añadir el directorio src al sys.path para permitir importaciones absolutas
#sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

def pytest_configure(config):
    env_file = find_dotenv('.env.test')
    load_dotenv(env_file)
    os.environ['FLASK_ENV'] = 'testing'
    print(f"Loaded environment variables from {env_file}")
    print(f"DB_USER: {os.getenv('DB_USER')}")
    print(f"DB_PASSWORD: {os.getenv('DB_PASSWORD')}")
    print(f"DB_HOST: {os.getenv('DB_HOST')}")
    print(f"DB_PORT: {os.getenv('DB_PORT')}")
    print(f"DB_NAME: {os.getenv('DB_NAME')}")
    print(f"APP_PORT: {os.getenv('APP_PORT')}")

@pytest.fixture(scope='module')
def test_client():
    from ..src.main import app, init_db 
    from ..src.models.database import db_session, base

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    with app.app_context():
        base.metadata.create_all(bind=db_session.bind)
        testing_client = app.test_client()
        yield testing_client
        base.metadata.drop_all(bind=db_session.bind)

@pytest.fixture(autouse=True)
def cleanup(test_client):
    from ..src.models.database import db_session, base
    with test_client.application.app_context():
        yield
        db_session.remove()
        base.metadata.drop_all(bind=db_session.bind)
        base.metadata.create_all(bind=db_session.bind)