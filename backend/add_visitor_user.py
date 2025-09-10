#!/usr/bin/env python3
"""
Script to add a VISITOR user to the database for testing.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

def add_visitor_user():
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if VISITOR user already exists
        visitor_user = db.query(User).filter(User.username == "VISITOR").first()
        if visitor_user:
            print("VISITOR user already exists:")
            print(f"Username: {visitor_user.username}")
            print(f"Email: {visitor_user.email}")
            print(f"User ID: {visitor_user.id}")
            return
        
        # Create VISITOR user
        visitor_user = User(
            username="VISITOR",
            email="visitor@example.com",
            hashed_password=get_password_hash("visitor123"),
            is_active=True
        )
        
        db.add(visitor_user)
        db.commit()
        db.refresh(visitor_user)
        
        print("VISITOR user created successfully!")
        print(f"Username: VISITOR")
        print(f"Password: visitor123")
        print(f"User ID: {visitor_user.id}")
        
        # Show all users in database
        users = db.query(User).all()
        print(f"\nAll users in database:")
        for user in users:
            print(f"  - {user.username} ({user.email}) - ID: {user.id}")
            
    except Exception as e:
        print(f"Error creating VISITOR user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_visitor_user()
