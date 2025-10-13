#!/usr/bin/env python3
"""
Simple test script to verify authentication works
"""

import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth():
    """Test authentication with the API"""
    print("Testing authentication...")
    
    # Test with form data
    data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data=data)
        print(f"Status Code: {response.status_code}")
        print(f"Response: {response.text}")
        
        if response.status_code == 200:
            token_data = response.json()
            print(f"Authentication successful!")
            print(f"Token type: {token_data['token_type']}")
            print(f"Access token: {token_data['access_token'][:50]}...")
            return token_data['access_token']
        else:
            print("Authentication failed")
            return None
            
    except Exception as e:
        print(f"Error during authentication test: {e}")
        return None

if __name__ == "__main__":
    test_auth()
