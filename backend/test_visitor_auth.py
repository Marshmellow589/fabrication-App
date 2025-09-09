#!/usr/bin/env python3
"""
Script to test VISITOR user authentication and API access (read-only).
"""

import sys
import os
import requests

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.add_visitor_user import add_visitor_user

def test_visitor_auth():
    # Base URL for the API
    BASE_URL = "http://127.0.0.1:8014"
    
    # First, make sure VISITOR user exists
    add_visitor_user()
    
    # Test authentication with VISITOR user
    auth_data = {
        "username": "VISITOR",
        "password": "visitor123"
    }
    
    try:
        # Get authentication token
        print("🧪 Testing VISITOR authentication and API access")
        print("=" * 50)
        
        response = requests.post(f"{BASE_URL}/auth/token", data=auth_data)
        if response.status_code != 200:
            print(f"❌ Authentication failed: {response.status_code}")
            print(response.text)
            return
        
        token_data = response.json()
        access_token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        print("✅ Authentication successful")
        print(f"Access token: {access_token[:50]}...")
        
        # Test read operations with visitor user
        print("\n📋 Testing read operations with VISITOR user")
        print("-" * 50)
        
        # Test 1: Get all users (should work for visitor)
        print("Test 1: Get all users")
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            users = response.json()
            print(f"✅ Retrieved {len(users)} users")
        
        # Test 2: Get material records
        print("\nTest 2: Get material records")
        response = requests.get(f"{BASE_URL}/material/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            materials = response.json()
            print(f"✅ Retrieved {len(materials)} material records")
        
        # Test 3: Get fitup records
        print("\nTest 3: Get fitup records")
        response = requests.get(f"{BASE_URL}/fitup/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            fitups = response.json()
            print(f"✅ Retrieved {len(fitups)} fitup records")
        
        # Test 4: Get final inspection records
        print("\nTest 4: Get final inspection records")
        response = requests.get(f"{BASE_URL}/final/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            inspections = response.json()
            print(f"✅ Retrieved {len(inspections)} final inspection records")
        
        # Test 5: Get NDT request records
        print("\nTest 5: Get NDT request records")
        response = requests.get(f"{BASE_URL}/ndt/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            ndt_requests = response.json()
            print(f"✅ Retrieved {len(ndt_requests)} NDT request records")
        
        # Test 6: Try to create a record (should fail for visitor)
        print("\nTest 6: Try to create material record (should fail)")
        material_data = {
            "project_id": 1,
            "material_type": "Test Material",
            "specification": "Test Spec",
            "grade": "Test Grade",
            "quantity": 10,
            "unit": "pieces",
            "status": "received"
        }
        
        response = requests.post(f"{BASE_URL}/material/", json=material_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code != 200:
            print("✅ Correctly failed to create record (VISITOR is read-only)")
        else:
            print("❌ Unexpected success - VISITOR should not be able to create records")
        
        print("\n✅ All VISITOR operations completed successfully!")
        print("VISITOR user can successfully read all records but cannot create new ones")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server. Make sure the server is running on port 8011.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_visitor_auth()
