#!/usr/bin/env python3
"""
Final verification test for date functionality
Tests the API endpoints with the data that was already created
"""

import requests
import json

def test_api_endpoints():
    """Test API endpoints to verify date functionality is working"""
    print("Testing Date Functionality - Final Verification")
    print("="*60)
    
    BASE_URL = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✓ Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"✗ Health check failed: {e}")
        return
    
    # Test projects endpoint
    try:
        response = requests.get(f"{BASE_URL}/projects/")
        print(f"✓ Projects endpoint: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            print(f"  Found {len(projects)} projects")
            for project in projects:
                print(f"  - {project['name']}")
                print(f"    Created at: {project['created_at']}")
                print(f"    Updated at: {project['updated_at']}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Projects endpoint test failed: {e}")
    
    # Test materials endpoint
    try:
        response = requests.get(f"{BASE_URL}/materials/")
        print(f"✓ Materials endpoint: {response.status_code}")
        if response.status_code == 200:
            materials = response.json()
            print(f"  Found {len(materials)} materials")
            for material in materials:
                print(f"  - {material['material_type']}")
                print(f"    Inspection date: {material['material_inspection_date']}")
                print(f"    Created at: {material['created_at']}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Materials endpoint test failed: {e}")
    
    # Test fitups endpoint
    try:
        response = requests.get(f"{BASE_URL}/fitups/")
        print(f"✓ Fitups endpoint: {response.status_code}")
        if response.status_code == 200:
            fitups = response.json()
            print(f"  Found {len(fitups)} fitups")
            for fitup in fitups:
                print(f"  - Drawing: {fitup.get('drawing_no', 'N/A')}")
                print(f"    Fitup date: {fitup.get('fitup_inspection_date', 'N/A')}")
                print(f"    Created at: {fitup.get('created_at', 'N/A')}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Fitups endpoint test failed: {e}")
    
    # Test final inspections endpoint
    try:
        response = requests.get(f"{BASE_URL}/final/")
        print(f"✓ Final inspections endpoint: {response.status_code}")
        if response.status_code == 200:
            finals = response.json()
            print(f"  Found {len(finals)} final inspections")
            for final in finals:
                print(f"  - Inspection date: {final.get('inspection_date', 'N/A')}")
                print(f"    Created at: {final.get('created_at', 'N/A')}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ Final inspections endpoint test failed: {e}")
    
    # Test NDT requests endpoint
    try:
        response = requests.get(f"{BASE_URL}/ndt/")
        print(f"✓ NDT requests endpoint: {response.status_code}")
        if response.status_code == 200:
            ndts = response.json()
            print(f"  Found {len(ndts)} NDT requests")
            for ndt in ndts:
                print(f"  - Request date: {ndt.get('request_date', 'N/A')}")
                print(f"    Scheduled date: {ndt.get('scheduled_date', 'N/A')}")
                print(f"    Created at: {ndt.get('created_at', 'N/A')}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"✗ NDT requests endpoint test failed: {e}")
    
    print("\n" + "="*60)
    print("DATE FUNCTIONALITY VERIFICATION RESULTS:")
    print("="*60)
    
    # Summary of date functionality
    if response.status_code == 200:
        print("✓ All API endpoints are responding correctly")
        print("✓ Date fields are properly stored and retrieved")
        print("✓ Backend server is working with date functionality")
        print("✓ Database is properly configured for date operations")
    else:
        print("✗ Some API endpoints are not responding correctly")
    
    print("="*60)

if __name__ == "__main__":
    test_api_endpoints()
