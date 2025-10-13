#!/usr/bin/env python3
"""
Debug script to test authentication directly
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.user import User
from backend.app.core.security import verify_password, get_password_hash

def debug_auth():
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Get the test user
        user = db.query(User).filter(User.username == "testuser").first()
        if not user:
            print("Test user not found!")
            return
        
        print(f"User found: {user.username}")
        print(f"User ID: {user.id}")
        print(f"User email: {user.email}")
        print(f"User is_active: {user.is_active}")
        print(f"User hashed_password: {user.hashed_password}")
        
        # Test password verification
        test_password = "testpassword"
        is_valid = verify_password(test_password, user.hashed_password)
        print(f"Password verification result: {is_valid}")
        
        # Test creating a new hash for comparison
        new_hash = get_password_hash(test_password)
        print(f"New hash for 'testpassword': {new_hash}")
        print(f"Original hash matches new hash: {user.hashed_password == new_hash}")
        
    except Exception as e:
        print(f"Error during debug: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    debug_auth()
