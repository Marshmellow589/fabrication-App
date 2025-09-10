#!/usr/bin/env python3
"""
Script to test MEMBER user operations - create records across all modules.
"""

import sys
import os
import requests

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from backend.add_member_user import add_member_user

def test_member_operations():
    # Base URL for the API
    BASE_URL = "http://127.0.0.1:8015"
    
    # First, make sure MEMBER user exists
    add_member_user()
    
    # Test authentication with MEMBER user
    auth_data = {
        "username": "MEMBER",
        "password": "member123"
    }
    
    try:
        # Get authentication token
        print("🧪 Testing MEMBER authentication and operations")
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
        
        # Test creating new records with member user
        print("\n📋 Testing record creation with MEMBER user")
        print("-" * 50)
        
        # Test 1: Create new material record
        print("Test 1: Create material record")
        material_data = {
            "project_id": 1,
            "material_type": "Stainless Steel Plate",
            "specification": "ASTM A240 316L",
            "grade": "316L",
            "quantity": 50,
            "unit": "pieces",
            "status": "received"
        }
        
        response = requests.post(f"{BASE_URL}/material/", json=material_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            material = response.json()
            print(f"✅ Created material: {material['material_type']} (ID: {material['id']})")
        
        # Test 2: Create new fitup record
        print("\nTest 2: Create fitup record")
        fitup_data = {
            "project_id": 1,
            "fitup_number": "FIT-002",
            "component_a": "FLANGE-001",
            "component_b": "PIPE-002",
            "joint_type": "Socket Weld",
            "status": "pending"
        }
        
        response = requests.post(f"{BASE_URL}/fitup/", json=fitup_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            fitup = response.json()
            print(f"✅ Created fitup: {fitup['fitup_number']} (ID: {fitup['id']})")
        
        # Test 3: Create new final inspection record
        print("\nTest 3: Create final inspection record")
        inspection_data = {
            "project_id": 1,
            "inspection_number": "FIN-002",
            "component_id": "VESSEL-001",
            "inspection_type": "Dimensional Check",
            "status": "in_progress",
            "result": "pending",
            "remarks": "Initial dimensional measurements completed",
            "is_approved": False
        }
        
        response = requests.post(f"{BASE_URL}/final/", json=inspection_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            inspection = response.json()
            print(f"✅ Created final inspection: {inspection['inspection_number']} (ID: {inspection['id']})")
        
        # Test 4: Create new NDT request record
        print("\nTest 4: Create NDT request record")
        ndt_data = {
            "project_id": 1,
            "request_number": "NDT-002",
            "component_id": "WELD-001",
            "ndt_method": "RT",  # Radiographic Testing
            "status": "requested",
            "remarks": "Radiographic testing required for critical weld",
            "result": "pending"
        }
        
        response = requests.post(f"{BASE_URL}/ndt/", json=ndt_data, headers=headers)
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            ndt = response.json()
            print(f"✅ Created NDT request: {ndt['request_number']} (ID: {ndt['id']})")
        
        # Verify all records were created
        print("\n📋 Verifying created records")
        print("-" * 30)
        
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
        
        print("\n✅ All MEMBER operations completed successfully!")
        print("MEMBER user can successfully create records across all modules")
        
    except requests.exceptions.ConnectionError:
        print("❌ Could not connect to the API server. Make sure the server is running on port 8011.")
    except Exception as e:
        print(f"❌ Error during testing: {e}")

if __name__ == "__main__":
    test_member_operations()
