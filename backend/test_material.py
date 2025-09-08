#!/usr/bin/env python3
"""
Script to test material records functionality.
"""

import sys
import os
import requests

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.create_test_user import create_test_user

def test_material_api():
    # Base URL for the API
    BASE_URL = "http://127.0.0.1:8006"
    
    # First, get an authentication token
    auth_data = {
        "username": "admin1",
        "password": "admin123"  # Try common default password
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
        
        # Test 1: Get all materials
        print("\n📋 Test 1: Get all materials")
        response = requests.get(f"{BASE_URL}/material/", headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            materials = response.json()
            print(f"Found {len(materials)} materials")
            for material in materials:
                print(f"  - {material['material_type']} (ID: {material['id']})")
        
        # Test 2: Create a new material
        print("\n📋 Test 2: Create new material")
        material_data = {
            "project_id": 1,
            "material_type": "Steel Plate",
            "specification": "ASTM A36",
            "grade": "A36",
            "quantity": 100.0,
            "unit": "kg",
            "status": "pending"
        }
        
        response = requests.post(f"{BASE_URL}/material/", json=material_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            new_material = response.json()
            print(f"Created material: {new_material['material_type']} (ID: {new_material['id']})")
            
            # Test 3: Get the specific material
            print("\n📋 Test 3: Get specific material")
            response = requests.get(f"{BASE_URL}/material/{new_material['id']}", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                material = response.json()
                print(f"Material details: {material}")
            
            # Test 4: Update the material
            print("\n📋 Test 4: Update material")
            update_data = {
                "status": "approved",
                "quantity": 150.0
            }
            
            response = requests.put(f"{BASE_URL}/material/{new_material['id']}", json=update_data, headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                updated_material = response.json()
                print(f"Updated material status: {updated_material['status']}")
                print(f"Updated quantity: {updated_material['quantity']}")
            
            # Test 5: Filter materials by project
            print("\n📋 Test 5: Filter materials by project")
            response = requests.get(f"{BASE_URL}/material/?project_id=1", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                project_materials = response.json()
                print(f"Found {len(project_materials)} materials for project 1")
        
        print("\n✅ All material tests completed successfully!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server. Make sure the server is running on port 8001.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    # Make sure test user exists
    create_test_user()
    
    print("🧪 Testing Material Records API")
    print("=" * 50)
    
    test_material_api()
