import uuid
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
from dotenv import load_dotenv


if os.path.exists('.env.test'):
    load_dotenv('.env.test')
else:
    load_dotenv('.env.development')


if os.getenv('FLASK_ENV') == 'testing':
    urldb = 'sqlite:///:memory:'  
else:
    userdb = os.environ["DB_USER"]
    password = os.environ["DB_PASSWORD"]
    host = os.environ["DB_HOST"]
    dbname = os.environ["DB_NAME"]
    port_db = os.environ["DB_PORT"]
    urldb = 'postgresql://' + userdb + ':' + password + '@' + host + ':' + port_db + '/' + dbname

engine = create_engine(urldb)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

base = declarative_base()

base.query = db_session.query_property()

def init_db():
    from .products import Category, Provider
    base.metadata.create_all(bind=engine)
    
    if not db_session.query(Category).filter_by(name = 'Electronic').first():
        electronic = Category(name = 'Electronic')
        db_session.add(electronic)

    if not db_session.query(Category).filter_by(name = 'Clothes').first(): 
        clothes = Category(name = 'Clothes')
        db_session.add(clothes)
            
    # Proveedor 1
    if not db_session.query(Provider).filter_by(name='Provider1').first():
        provider1 = Provider(
            name='Provider1',
            country='Country1',
            contact='Contact1',
            telephone='1234567890',
            email='provider1@example.com'
        )
        db_session.add(provider1)

    # Proveedor 2
    if not db_session.query(Provider).filter_by(name='Provider2').first():
        provider2 = Provider(
            name='Provider2',
            country='Country2',
            contact='Contact2',
            telephone='0987654321',
            email='provider2@example.com'
        )
        db_session.add(provider2)

    db_session.commit()