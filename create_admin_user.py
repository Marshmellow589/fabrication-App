#!/usr/bin/env python3
"""
Script to create an admin user with username 'admin' and password 'admin123'
"""

import sys
import os

# Add the backend directory to Python path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from backend.app.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

def create_admin_user():
    """Create an admin user with specified credentials"""
    db = SessionLocal()
    
    try:
        # Check if admin user already exists
        existing_admin = db.query(User).filter(User.username == "admin").first()
        if existing_admin:
            print("⚠️ Admin user already exists")
            print(f"Username: {existing_admin.username}")
            print(f"Role: {existing_admin.role}")
            return
        
        # Create new admin user
        admin_user = User(
            username="admin",
            email="admin@fabrication.com",
            full_name="System Administrator",
            hashed_password=get_password_hash("admin123"),
            role="admin",
            is_active=True,
            is_superuser=True,
            created_by=1  # Assuming user ID 1 exists
        )
        
        db.add(admin_user)
        db.commit()
        db.refresh(admin_user)
        
        print("✅ Admin user created successfully!")
        print(f"Username: admin")
        print(f"Password: admin123")
        print(f"Role: admin")
        print(f"Email: admin@fabrication.com")
        
    except Exception as e:
        print(f"❌ Error creating admin user: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    print("👑 Creating Admin User...")
    create_admin_user()
