#!/usr/bin/env python3
"""
Simple test to verify admin2 login works
"""

import requests
import json

def test_admin_login():
    """Test admin2 login with the new password"""
    BASE_URL = "http://localhost:8000"
    
    print("Testing admin2 login...")
    data = {
        "username": "admin2",
        "password": "admin1234",
        "username": "admin1",
        "password": "admin1234"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data=data)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"✓ Login successful!")
            print(f"Token type: {token_data['token_type']}")
            print(f"Access token: {token_data['access_token'][:50]}...")
            
            # Test accessing a protected endpoint
            headers = {"Authorization": f"Bearer {token_data['access_token']}"}
            projects_response = requests.get(f"{BASE_URL}/projects/", headers=headers)
            print(f"Projects endpoint status: {projects_response.status_code}")
            
            if projects_response.status_code == 200:
                print("✓ Successfully accessed protected endpoint!")
                return True
            else:
                print(f"✗ Failed to access protected endpoint: {projects_response.text}")
                return False
                
        else:
            print(f"✗ Login failed: {response.text}")
            return False
            
    except Exception as e:
        print(f"Error during login test: {e}")
        return False

if __name__ == "__main__":
    test_admin_login()
