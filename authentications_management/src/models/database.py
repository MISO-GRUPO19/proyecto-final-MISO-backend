from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
from dotenv import load_dotenv

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
    from .users import Users, Role

    base.metadata.create_all(bind=engine)

    if not db_session.query(Users).filter_by(email='admin@ccp.com').first():
        admin = Users(email='admin@ccp.com', password='Admin123-', role=Role.Administrador)
        db_session.add(admin)
    
    if not db_session.query(Users).filter_by(email='vendedor@ccp.com').first():
        vendedor = Users(email='vendedor@ccp.com', password='Vendedor123-', role=Role.Vendedor)
        db_session.add(vendedor)
    
    if not db_session.query(Users).filter_by(email='cliente@ccp.com').first():
        cliente = Users(email='cliente@ccp.com', password='Cliente123-', role=Role.Cliente)
        db_session.add(cliente)

    db_session.commit()