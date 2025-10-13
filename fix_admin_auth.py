#!/usr/bin/env python3
"""
Script to fix admin authentication by resetting the admin2 password
"""

import sys
import os

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal
from backend.app.models.user import User
from backend.app.core.security import get_password_hash

def reset_admin_password():
    """Reset admin2 password to admin123"""
    db = SessionLocal()
    try:
        # Find the admin2 user
        admin_user = db.query(User).filter(User.username == "admin2").first()
        if not admin_user:
            print("admin2 user not found!")
            return False
        
        print(f"Found admin2 user: ID={admin_user.id}, username={admin_user.username}")
        print(f"Current hashed password: {admin_user.hashed_password}")
        
        # Reset the password
        new_password = "admin123"
        admin_user.hashed_password = get_password_hash(new_password)
        
        db.commit()
        print(f"Password reset successfully for admin2")
        print(f"New password: {new_password}")
        print(f"New hashed password: {admin_user.hashed_password}")
        
        return True
        
    except Exception as e:
        print(f"Error resetting admin password: {e}")
        db.rollback()
        return False
    finally:
        db.close()

def test_admin_login():
    """Test admin2 login with the new password"""
    import requests
    
    BASE_URL = "http://localhost:8000"
    
    print("\nTesting admin2 login...")
    data = {
        "username": "admin2",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data=data)
        print(f"Login attempt status: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✓ Login successful!")
            print(f"Token type: {token_data['token_type']}")
            print(f"Access token: {token_data['access_token'][:50]}...")
            return True
        else:
            print("✗ Login failed")
            return False
            
    except Exception as e:
        print(f"Error during login test: {e}")
        return False

if __name__ == "__main__":
    print("Fixing Admin Authentication")
    print("=" * 40)
    
    # Reset admin password
    if reset_admin_password():
        # Test the login
        test_admin_login()
    else:
        print("Failed to reset admin password")
