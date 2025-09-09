#!/usr/bin/env python3
"""
Script to add a MEMBER user to the database for testing.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

def add_member_user():
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if MEMBER user already exists
        member_user = db.query(User).filter(User.username == "MEMBER").first()
        if member_user:
            print("MEMBER user already exists:")
            print(f"Username: {member_user.username}")
            print(f"Email: {member_user.email}")
            print(f"User ID: {member_user.id}")
            return
        
        # Create MEMBER user
        member_user = User(
            username="MEMBER",
            email="member@example.com",
            hashed_password=get_password_hash("member123"),
            is_active=True
        )
        
        db.add(member_user)
        db.commit()
        db.refresh(member_user)
        
        print("MEMBER user created successfully!")
        print(f"Username: MEMBER")
        print(f"Password: member123")
        print(f"User ID: {member_user.id}")
        
        # Show all users in database
        users = db.query(User).all()
        print(f"\nAll users in database:")
        for user in users:
            print(f"  - {user.username} ({user.email}) - ID: {user.id}")
            
    except Exception as e:
        print(f"Error creating MEMBER user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_member_user()
