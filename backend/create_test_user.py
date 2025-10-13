#!/usr/bin/env python3
"""
Script to create a test user for authentication testing.
Run this script to create a test user in the database.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models.user import User
from app.core.security import get_password_hash

def create_test_user():
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if test user already exists
        existing_user = db.query(User).filter(User.username == "testuser").first()
        if existing_user:
            print("Test user already exists:")
            print(f"Username: testuser")
            print(f"Password: testpassword")
            print(f"User ID: {existing_user.id}")
            return
        
        # Create test user
        test_user = User(
            username="testuser",
            email="testuser@example.com",
            hashed_password=get_password_hash("testpassword"),
            is_active=True
        )
        
        db.add(test_user)
        db.commit()
        db.refresh(test_user)
        
        print("Test user created successfully!")
        print(f"Username: testuser")
        print(f"Password: testpassword")
        print(f"User ID: {test_user.id}")
        
    except Exception as e:
        print(f"Error creating test user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_test_user()
