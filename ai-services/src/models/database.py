from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
from dotenv import load_dotenv

loaded = load_dotenv('.env.development')

# Configuración de la conexión a la base de datos
if os.getenv('FLASK_ENV') == 'testing':
    urldb = 'sqlite:///:memory:'
    engine = create_engine(
        urldb,
        connect_args={"check_same_thread": False},
        echo=False
    )
else:
    userdb = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    dbname = os.environ["DB_NAME"]
    port_db = os.environ["DB_PORT"]
    urldb = f'postgresql://{userdb}:{password}@{host}:{port_db}/{dbname}'
    engine = create_engine(
        urldb,
        pool_size=25,
        max_overflow=10,
        pool_timeout=10,
        pool_recycle=180,
        pool_pre_ping=True,
        echo=False
    )
    
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

base = declarative_base()

base.query = db_session.query_property()

def init_db():
    base.metadata.create_all(bind=engine)