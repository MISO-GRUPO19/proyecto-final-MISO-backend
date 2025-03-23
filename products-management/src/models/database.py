from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os
from dotenv import load_dotenv

loaded = load_dotenv('.env.development')

if os.environ.get("DATABASE_URL") is None:
    userdb = "postgres"
    password = "postgres"
    host = "localhost"
    dbname = "products"
    port_db="5433"
    urldb = 'postgresql://' + userdb + ':' + password + '@' + host+ ':' +port_db + '/' + dbname
else:
    urldb = os.environ.get("DATABASE_URL")
    
engine = create_engine(urldb)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

base = declarative_base()

base.query = db_session.query_property()

def init_db():
    base.metadata.create_all(bind=engine)