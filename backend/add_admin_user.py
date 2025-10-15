#!/usr/bin/env python3
"""
Script to add an ADMIN user to the database for testing admin functions.
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.user import User, UserRole
from backend.app.core.security import get_password_hash

def add_admin_user():
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Check if admin2 user already exists
        admin_user = db.query(User).filter(User.username == "admin2").first()
        if admin_user:
            print("admin2 user already exists:")
            print(f"Username: {admin_user.username}")
            print(f"Email: {admin_user.email}")
            print(f"User ID: {admin_user.id}")
            return
        
        # Create admin2 user
        admin_user = User(
            username="admin2",
            email="admin2@example.com",
            hashed_password=get_password_hash("admin123"),
            full_name="Administrator User",
            role=UserRole.ADMIN,
            is_active=True,
            is_superuser=True  # Make this an admin user
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("admin2 user created successfully!")
        print(f"Username: admin2")
        print(f"Password: admin123")
        print(f"User ID: {admin_user.id}")
        print(f"Is Superuser: {admin_user.is_superuser}")
        print(f"Role: {admin_user.role}")
        
        # Show all users in database
        users = db.query(User).all()
        print(f"\nAll users in database:")
        for user in users:
            print(f"  - {user.username} ({user.email}) - ID: {user.id} - Role: {user.role} - Superuser: {user.is_superuser}")
            
    except Exception as e:
        print(f"Error creating admin2 user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    add_admin_user()
