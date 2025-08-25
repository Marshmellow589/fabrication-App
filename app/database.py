from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models.base import Base

# Create a database engine
engine = create_engine('sqlite:///./db.sqlite')

# Create a configured "Session" class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    """Dependency for getting DB session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
