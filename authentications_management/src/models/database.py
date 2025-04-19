from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base
import os
from dotenv import load_dotenv

load_dotenv('.env.development')

# Configuración de la conexión a la base de datos
if os.getenv('FLASK_ENV') == 'testing':
    urldb = 'sqlite:///:memory:'  
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

db_session = scoped_session(sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
))

base = declarative_base()
base.query = db_session.query_property()

def init_db():
    from .users import Users, Role
    from .customers import Customers
    from .sellers import Sellers

    base.metadata.create_all(bind=engine)

    try:
        # Crear datos iniciales
        if not db_session.query(Users).filter_by(email='admin@ccp.com').first():
            admin = Users(email='admin@ccp.com', password='Admin123-', role=Role.Administrador)
            db_session.add(admin)
        
        if not db_session.query(Users).filter_by(email='vendedor@ccp.com').first():
            vendedor = Users(email='vendedor@ccp.com', password='Vendedor123-', role=Role.Vendedor)
            seller = Sellers(
                identification='123456789',
                country='Colombia',
                address='Calle 123 #45-67',
                telephone='3001234567',
                name='Juan Pérez',
                email='vendedor@ccp.com')
            db_session.add(seller)
            db_session.add(vendedor)
            
        if not db_session.query(Users).filter_by(email='cliente@ccp.com').first():
            cliente = Users(email='cliente@ccp.com', password='Cliente123-', role=Role.Cliente)
            customer = Customers(
                country='Colombia',
                address='Calle Falsa 123',
                phoneNumber='3007654321',
                firstName='Ana',
                lastName='Gómez',
                email='cliente@ccp.com')
            db_session.add(customer)
            db_session.add(cliente)
        
        db_session.commit()
    except Exception as e:
        db_session.rollback()
        print(f"Error inicializando la base de datos: {str(e)}")
        raise
    finally:
        db_session.remove()