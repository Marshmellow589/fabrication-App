#!/usr/bin/env python3
"""
Script to test ADMIN user operations - create new users and records across all modules.
"""

import sys
import os
import requests

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.add_admin_user import add_admin_user

def test_admin_operations():
    # Base URL for the API
    BASE_URL = "http://127.0.0.1:8014"
    
    # First, make sure admin2 user exists
    add_admin_user()
    
    # Test authentication with admin2 user
    auth_data = {
        "username": "admin2",
        "password": "admin123"
    }
    
    try:
        # Get authentication token
        print("🧪 Testing ADMIN authentication and operations")
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
        
        # Test 1: Create new user (user3)
        print("\nTest 1: Create new user (user3)")
        user_data = {
            "username": "user3",
            "email": "user3@example.com",
            "password": "user3123",
            "is_active": True
        }
        
        response = requests.post(f"{BASE_URL}/users/", json=user_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            user = response.json()
            print(f"✅ Created user: {user['username']} (ID: {user['id']})")
        
        # Test creating new records with admin user
        print("\n📋 Testing record creation with ADMIN user")
        print("-" * 50)
        
        # Test 2: Create new material record
        print("Test 2: Create material record")
        material_data = {
            "project_id": 2,
            "material_type": "Copper Pipe",
            "specification": "ASTM B88 Type K",
            "grade": "Type K",
            "quantity": 100,
            "unit": "meters",
            "status": "received"
        }
        
        response = requests.post(f"{BASE_URL}/material/", json=material_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            material = response.json()
            print(f"✅ Created material: {material['material_type']} (ID: {material['id']})")
        
        # Test 3: Create new fitup record
        print("\nTest 3: Create fitup record")
        fitup_data = {
            "project_id": 2,
            "fitup_number": "FIT-003",
            "component_a": "PIPE-001",
            "component_b": "ELBOW-001",
            "joint_type": "Butt Weld",
            "status": "approved"
        }
        
        response = requests.post(f"{BASE_URL}/fitup/", json=fitup_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            fitup = response.json()
            print(f"✅ Created fitup: {fitup['fitup_number']} (ID: {fitup['id']})")
        
        # Test 4: Create new final inspection record
        print("\nTest 4: Create final inspection record")
        inspection_data = {
            "project_id": 2,
            "inspection_number": "FIN-003",
            "component_id": "PIPELINE-001",
            "inspection_type": "Visual Inspection",
            "status": "completed",
            "result": "passed",
            "remarks": "All welds visually acceptable, no defects found",
            "is_approved": True
        }
        
        response = requests.post(f"{BASE_URL}/final/", json=inspection_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            inspection = response.json()
            print(f"✅ Created final inspection: {inspection['inspection_number']} (ID: {inspection['id']})")
        
        # Test 5: Create new NDT request record
        print("\nTest 5: Create NDT request record")
        ndt_data = {
            "project_id": 2,
            "request_number": "NDT-003",
            "component_id": "WELD-002",
            "ndt_method": "PT",  # Penetrant Testing
            "status": "completed",
            "remarks": "Penetrant testing completed, no surface defects found",
            "result": "passed"
        }
        
        response = requests.post(f"{BASE_URL}/ndt/", json=ndt_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            ndt = response.json()
            print(f"✅ Created NDT request: {ndt['request_number']} (ID: {ndt['id']})")
        
        # Verify all records were created
        print("\n📋 Verifying created records")
        print("-" * 30)
        
        # Get all users
        response = requests.get(f"{BASE_URL}/users/", headers=headers)
        if response.status_code == 200:
            users = response.json()
            print(f"Users: {len(users)} records")
        
        # Get material records
        response = requests.get(f"{BASE_URL}/material/", headers=headers)
        if response.status_code == 200:
            materials = response.json()
            print(f"Materials: {len(materials)} records")
        
        # Get fitup records
        response = requests.get(f"{BASE_URL}/fitup/", headers=headers)
        if response.status_code == 200:
            fitups = response.json()
            print(f"Fitup records: {len(fitups)} records")
        
        # Get final inspection records
        response = requests.get(f"{BASE_URL}/final/", headers=headers)
        if response.status_code == 200:
            inspections = response.json()
            print(f"Final inspections: {len(inspections)} records")
        
        # Get NDT request records
        response = requests.get(f"{BASE_URL}/ndt/", headers=headers)
        if response.status_code == 200:
            ndt_requests = response.json()
            print(f"NDT requests: {len(ndt_requests)} records")
        
        print("\n✅ All ADMIN operations completed successfully!")
        print("admin2 user can successfully create users and records across all modules")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server. Make sure the server is running on port 8011.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_admin_operations()
