from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from fabrication_app.app.routers import material, fit_up, final, ndt, auth
from fabrication_app.app.database import engine, Base

app = FastAPI()

# Setup CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create database tables with robust initialization
import logging
import os
from sqlalchemy import inspect

logger = logging.getLogger(__name__)

def initialize_database():
    # Get absolute path to database file
    db_path = os.path.abspath("fabrication_app/app/database.db")
    logger.info(f"Database path: {db_path}")
    
    # Check if database exists and is accessible
    if not os.path.exists(db_path):
        logger.info("Creating new database...")
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("Database created successfully")
        except Exception as e:
            logger.error(f"Failed to create database: {e}")
            raise
    else:
        logger.info("Using existing database")
        try:
            # Only create tables that don't exist
            inspector = inspect(engine)
            existing_tables = set(inspector.get_table_names())
            needed_tables = set(Base.metadata.tables.keys())
            
            tables_to_create = needed_tables - existing_tables
            if tables_to_create:
                logger.info(f"Creating missing tables: {tables_to_create}")
                for table_name in tables_to_create:
                    table = Base.metadata.tables[table_name]
                    table.create(bind=engine)
        except Exception as e:
            logger.error(f"Database initialization failed: {e}")
            raise

initialize_database()

# Include routers
app.include_router(material.router)
app.include_router(fit_up.router)
app.include_router(final.router)
app.include_router(ndt.router)
app.include_router(auth.router)

@app.get("/")
def read_root():
    return {"message": "Fabrication Inspection API"}
