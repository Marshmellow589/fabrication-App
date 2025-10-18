#!/usr/bin/env python3
"""
Database recreation script to fix schema issues
"""

import os
import sys

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import engine, Base
from backend.app.models import user, project, material, fitup, final_inspection, ndt_request, audit_trail, user_project_assignment

def recreate_database():
    """Drop and recreate all database tables"""
    print("🗑️  Dropping existing tables...")
    Base.metadata.drop_all(bind=engine)
    
    print("🔄 Creating new tables...")
    Base.metadata.create_all(bind=engine)
    
    print("✅ Database tables recreated successfully!")

if __name__ == "__main__":
    recreate_database()
