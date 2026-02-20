from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .main import psycopg2

# Use SQLAlchemy's correct dialect name: postgresql (not postgres)
# and specify a driver. psycopg (v3) is recommended on modern Python.
SQLALCHEMY_DATABASE_URL = "postgresql+psycopg2://postgres:root@localhost:5432/fastApi"

engine = create_engine(SQLALCHEMY_DATABASE_URL, pool_pre_ping=True)

SessionLocal = sessionmaker(autocommit = False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()