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
    base.metadata.create_all(bind=engine)