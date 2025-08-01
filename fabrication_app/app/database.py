import os
import tempfile
import logging
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import tempfile
import logging

logger = logging.getLogger(__name__)

SQLALCHEMY_DATABASE_URL = "sqlite:///./fabrication_app/app/database.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    pool_pre_ping=True
)

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    try:
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")
        cursor.close()
    except Exception as e:
        logger.error(f"Failed to set SQLite PRAGMA: {str(e)}")

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Import models after Base is defined to avoid circular imports
from fabrication_app.app.models.user import User
from fabrication_app.app.models.material import MaterialInspection
from fabrication_app.app.models.fit_up import FitUpInspection
from fabrication_app.app.models.final import FinalInspection
from fabrication_app.app.models.ndt import NDTRequest

def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database error: {str(e)}")
        db.rollback()
        raise
    finally:
        db.close()
