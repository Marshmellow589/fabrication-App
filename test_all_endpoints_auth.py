#!/usr/bin/env python3
"""
Test all protected endpoints to verify authentication is working correctly
"""

import requests
import json

def get_auth_token():
    """Get authentication token"""
    BASE_URL = "http://localhost:8000"
    
    data = {
        "username": "admin2",
        "password": "admin123"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/auth/token", data=data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data['access_token']
        else:
            print(f"Failed to get token: {response.status_code} - {response.text}")
            return None
    except Exception as e:
        print(f"Error getting token: {e}")
        return None

def test_protected_endpoints(token):
    """Test all protected endpoints with the authentication token"""
    BASE_URL = "http://localhost:8000"
    headers = {"Authorization": f"Bearer {token}"}
    
    endpoints_to_test = [
        "/projects/",
        "/materials/",
        "/fitups/",
        "/final/",
        "/ndt/",
        "/users/",
        "/dashboard/",
        "/audit-trail/"
    ]
    
    print("Testing Protected Endpoints")
    print("=" * 50)
    
    all_successful = True
    
    for endpoint in endpoints_to_test:
        try:
            response = requests.get(f"{BASE_URL}{endpoint}", headers=headers)
            print(f"{endpoint}: {response.status_code}")
            
            if response.status_code == 200:
                print(f"  ✓ Success - {len(response.json()) if response.text else 'Empty'} records")
            elif response.status_code == 401:
                print(f"  ✗ Authentication failed")
                all_successful = False
            elif response.status_code == 404:
                print(f"  ⚠ Endpoint not found (might be expected)")
            else:
                print(f"  ✗ Failed with status {response.status_code}")
                all_successful = False
                
        except Exception as e:
            print(f"{endpoint}: Error - {e}")
            all_successful = False
    
    return all_successful

def test_update_operations(token):
    """Test update operations for final inspection and NDT"""
    BASE_URL = "http://localhost:8000"
    headers = {"Authorization": f"Bearer {token}"}
    
    print("\nTesting Update Operations")
    print("=" * 50)
    
    # Test final inspection endpoints
    try:
        # First get existing final inspections
        response = requests.get(f"{BASE_URL}/final/", headers=headers)
        if response.status_code == 200:
            final_inspections = response.json()
            if final_inspections:
                inspection_id = final_inspections[0]['id']
                print(f"Testing update on final inspection ID: {inspection_id}")
                
                # Test update
                update_data = {
                    "status": "updated_test"
                }
                update_response = requests.put(
                    f"{BASE_URL}/final/{inspection_id}",
                    headers=headers,
                    json=update_data
                )
                print(f"Final inspection update: {update_response.status_code}")
                if update_response.status_code == 200:
                    print("  ✓ Final inspection update successful")
                else:
                    print(f"  ✗ Final inspection update failed: {update_response.text}")
            else:
                print("No final inspections found to test update")
        else:
            print(f"Failed to get final inspections: {response.status_code}")
    except Exception as e:
        print(f"Final inspection test error: {e}")
    
    # Test NDT endpoints
    try:
        # First get existing NDT requests
        response = requests.get(f"{BASE_URL}/ndt/", headers=headers)
        if response.status_code == 200:
            ndt_requests = response.json()
            if ndt_requests:
                ndt_id = ndt_requests[0]['id']
                print(f"Testing update on NDT request ID: {ndt_id}")
                
                # Test update
                update_data = {
                    "status": "updated_test"
                }
                update_response = requests.put(
                    f"{BASE_URL}/ndt/{ndt_id}",
                    headers=headers,
                    json=update_data
                )
                print(f"NDT request update: {update_response.status_code}")
                if update_response.status_code == 200:
                    print("  ✓ NDT request update successful")
                else:
                    print(f"  ✗ NDT request update failed: {update_response.text}")
            else:
                print("No NDT requests found to test update")
        else:
            print(f"Failed to get NDT requests: {response.status_code}")
    except Exception as e:
        print(f"NDT test error: {e}")

def main():
    print("Comprehensive Authentication Test")
    print("=" * 60)
    
    # Get authentication token
    token = get_auth_token()
    if not token:
        print("Failed to get authentication token")
        return
    
    print(f"✓ Authentication token obtained successfully")
    print(f"Token: {token[:50]}...")
    
    # Test all protected endpoints
    endpoints_success = test_protected_endpoints(token)
    
    # Test update operations
    test_update_operations(token)
    
    print("\n" + "=" * 60)
    print("AUTHENTICATION TEST RESULTS:")
    print("=" * 60)
    
    if endpoints_success:
        print("✓ All protected endpoints are accessible with authentication")
        print("✓ Authentication system is working correctly")
        print("✓ Frontend should be able to access all endpoints with proper token")
    else:
        print("✗ Some endpoints failed authentication")
        print("✗ Check frontend token handling and API configuration")
    
    print("=" * 60)

if __name__ == "__main__":
    main()
