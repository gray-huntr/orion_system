from myapp import myapp as app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# engine = create_engine(f'mysql://{app.config.DB_USERNAME}@{app.config.DB_HOST}/{app.config.DB_NAME}')
engine = create_engine(f'mysql://root@localhost/orion_system')

Session = sessionmaker(bind=engine)
session = Session()

Base = declarative_base()

def setup_db():
    print("Setups")
    Base.metadata.create_all(engine)

