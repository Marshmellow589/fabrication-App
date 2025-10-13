#!/usr/bin/env python3
"""
Test script to verify date functionality in the backend API
"""

import requests
import json
from datetime import datetime, timedelta

BASE_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_authentication():
    """Test authentication"""
    try:
        data = {
            "username": "testuser",
            "password": "testpassword"
        }
        response = requests.post(f"{BASE_URL}/auth/token", data=data)
        if response.status_code == 200:
            token_data = response.json()
            print(f"Authentication successful: {token_data['token_type']}")
            return token_data['access_token']
        else:
            print(f"Authentication failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Authentication test failed: {e}")
        return None

def test_project_creation(token):
    """Test project creation with date fields"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    project_data = {
        "name": "Test Project with Dates",
        "description": "Testing date functionality",
        "start_date": (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d"),
        "end_date": (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        "status": "active"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/projects/", json=project_data, headers=headers)
        if response.status_code == 200:
            project = response.json()
            print(f"Project created successfully: {project['name']}")
            print(f"Start date: {project['start_date']}")
            print(f"End date: {project['end_date']}")
            return project
        else:
            print(f"Project creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Project creation test failed: {e}")
        return None

def test_material_creation(token, project_id):
    """Test material creation with date fields"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    material_data = {
        "project_id": project_id,
        "material_name": "Test Steel Plate",
        "material_type": "Steel",
        "quantity": 10,
        "unit": "pieces",
        "inspection_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "approved",
        "inspector": "Test Inspector",
        "notes": "Testing date functionality in material inspection"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/materials/", json=material_data, headers=headers)
        if response.status_code == 200:
            material = response.json()
            print(f"Material created successfully: {material['material_name']}")
            print(f"Inspection date: {material['inspection_date']}")
            return material
        else:
            print(f"Material creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Material creation test failed: {e}")
        return None

def test_fitup_creation(token, project_id):
    """Test fitup creation with date fields"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    fitup_data = {
        "project_id": project_id,
        "component_name": "Test Component",
        "fitup_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "completed",
        "inspector": "Test Inspector",
        "notes": "Testing date functionality in fitup inspection"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/fitups/", json=fitup_data, headers=headers)
        if response.status_code == 200:
            fitup = response.json()
            print(f"Fitup created successfully: {fitup['component_name']}")
            print(f"Fitup date: {fitup['fitup_date']}")
            return fitup
        else:
            print(f"Fitup creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Fitup creation test failed: {e}")
        return None

def test_final_inspection_creation(token, project_id):
    """Test final inspection creation with date fields"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    final_data = {
        "project_id": project_id,
        "inspection_date": datetime.now().strftime("%Y-%m-%d"),
        "status": "passed",
        "inspector": "Test Inspector",
        "notes": "Testing date functionality in final inspection"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/final/", json=final_data, headers=headers)
        if response.status_code == 200:
            final = response.json()
            print(f"Final inspection created successfully")
            print(f"Inspection date: {final['inspection_date']}")
            return final
        else:
            print(f"Final inspection creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Final inspection creation test failed: {e}")
        return None

def test_ndt_request_creation(token, project_id):
    """Test NDT request creation with date fields"""
    headers = {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}
    
    ndt_data = {
        "project_id": project_id,
        "request_date": datetime.now().strftime("%Y-%m-%d"),
        "scheduled_date": (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d"),
        "technique": "UT",
        "status": "scheduled",
        "requested_by": "Test Inspector",
        "notes": "Testing date functionality in NDT request"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/ndt/", json=ndt_data, headers=headers)
        if response.status_code == 200:
            ndt = response.json()
            print(f"NDT request created successfully")
            print(f"Request date: {ndt['request_date']}")
            print(f"Scheduled date: {ndt['scheduled_date']}")
            return ndt
        else:
            print(f"NDT request creation failed: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"NDT request creation test failed: {e}")
        return None

def main():
    """Main test function"""
    print("Testing Date Functionality in Backend API")
    print("=" * 50)
    
    # Test health endpoint
    if not test_health():
        print("Health check failed. Make sure the backend server is running.")
        return
    
    # Test authentication
    token = test_authentication()
    if not token:
        print("Authentication failed. Cannot proceed with other tests.")
        return
    
    print("\n" + "=" * 50)
    print("Testing Date Field Creation")
    print("=" * 50)
    
    # Test project creation
    project = test_project_creation(token)
    if not project:
        print("Project creation failed. Cannot proceed with other tests.")
        return
    
    # Test other entities with date fields
    test_material_creation(token, project['id'])
    test_fitup_creation(token, project['id'])
    test_final_inspection_creation(token, project['id'])
    test_ndt_request_creation(token, project['id'])
    
    print("\n" + "=" * 50)
    print("Date functionality test completed!")
    print("=" * 50)

if __name__ == "__main__":
    main()
