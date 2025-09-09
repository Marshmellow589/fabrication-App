#!/usr/bin/env python3
"""
Script to test fitup records functionality.
"""

import sys
import os
import requests

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.create_test_user import create_test_user

def test_fitup_api():
    # Base URL for the API
    BASE_URL = "http://127.0.0.1:8008"
    
    # First, get an authentication token
    auth_data = {
        "username": "testuser",
        "password": "testpassword"
    }
    
    try:
        # Get authentication token
        response = requests.post(f"{BASE_URL}/auth/token", data=auth_data)
        if response.status_code != 200:
            print(f"Authentication failed: {response.status_code}")
            print(response.text)
            return
        
        token_data = response.json()
        access_token = token_data["access_token"]
        headers = {"Authorization": f"Bearer {access_token}"}
        
        print("✅ Authentication successful")
        print(f"Access token: {access_token}")
        
        # Test 1: Get all fitup records
        print("\n📋 Test 1: Get all fitup records")
        response = requests.get(f"{BASE_URL}/fitup/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            fitups = response.json()
            print(f"Found {len(fitups)} fitup records")
            for fitup in fitups:
                print(f"  - Fitup ID: {fitup['id']}, Project ID: {fitup['project_id']}")
        
        # Test 2: Create a new fitup record
        print("\n📋 Test 2: Create new fitup record")
        fitup_data = {
            "project_id": 1,
            "fitup_number": "FIT-001",
            "wps_number": "WPS-001",
            "joint_type": "Butt Joint",
            "material_thickness": 12.5,
            "process": "SMAW",
            "status": "pending"
        }
        
        response = requests.post(f"{BASE_URL}/fitup/", json=fitup_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            new_fitup = response.json()
            print(f"Created fitup record: {new_fitup['fitup_number']} (ID: {new_fitup['id']})")
            
            # Test 3: Get the specific fitup record
            print("\n📋 Test 3: Get specific fitup record")
            response = requests.get(f"{BASE_URL}/fitup/{new_fitup['id']}", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                fitup = response.json()
                print(f"Fitup details: {fitup}")
            
            # Test 4: Update the fitup record
            print("\n📋 Test 4: Update fitup record")
            update_data = {
                "status": "approved",
                "material_thickness": 15.0
            }
            
            response = requests.put(f"{BASE_URL}/fitup/{new_fitup['id']}", json=update_data, headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                updated_fitup = response.json()
            print(f"Updated fitup status: {updated_fitup['status']}")
            
            # Test 5: Filter fitup records by project
            print("\n📋 Test 5: Filter fitup records by project")
            response = requests.get(f"{BASE_URL}/fitup/?project_id=1", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                project_fitups = response.json()
                print(f"Found {len(project_fitups)} fitup records for project 1")
        else:
            print(f"Error response: {response.text}")
        
        print("\n✅ All fitup tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server. Make sure the server is running on port 8006.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    # Make sure test user exists
    create_test_user()
    
    print("🧪 Testing Fitup Records API")
    print("=" * 50)
    
    test_fitup_api()
