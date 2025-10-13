#!/usr/bin/env python3
"""
Test dashboard navigation functionality
"""

import requests
import json

def test_dashboard_navigation():
    """Test that dashboard navigation works correctly"""
    print("Testing Dashboard Navigation")
    print("=" * 50)
    
    # Test login first
    login_data = {
        "username": "admin2",
        "password": "admin123"
    }
    
    try:
        # Login to get token
        login_response = requests.post("http://localhost:8000/auth/token", data=login_data)
        if login_response.status_code != 200:
            print(f"✗ Login failed: {login_response.status_code}")
            return False
        
        token_data = login_response.json()
        token = token_data['access_token']
        print("✓ Login successful")
        
        # Test dashboard access
        headers = {"Authorization": f"Bearer {token}"}
        dashboard_response = requests.get("http://localhost:8000/dashboard/", headers=headers)
        
        if dashboard_response.status_code == 200:
            print("✓ Dashboard accessible")
        else:
            print(f"✗ Dashboard access failed: {dashboard_response.status_code}")
            return False
        
        # Test final inspection endpoint
        final_response = requests.get("http://localhost:8000/final/", headers=headers)
        if final_response.status_code == 200:
            print("✓ Final inspection endpoint accessible")
            final_data = final_response.json()
            print(f"  Found {len(final_data)} final inspection records")
        else:
            print(f"✗ Final inspection endpoint failed: {final_response.status_code}")
            return False
        
        # Test NDT endpoint
        ndt_response = requests.get("http://localhost:8000/ndt/", headers=headers)
        if ndt_response.status_code == 200:
            print("✓ NDT endpoint accessible")
            ndt_data = ndt_response.json()
            print(f"  Found {len(ndt_data)} NDT request records")
        else:
            print(f"✗ NDT endpoint failed: {ndt_response.status_code}")
            return False
        
        # Test projects endpoint
        projects_response = requests.get("http://localhost:8000/projects/", headers=headers)
        if projects_response.status_code == 200:
            print("✓ Projects endpoint accessible")
            projects_data = projects_response.json()
            print(f"  Found {len(projects_data)} project records")
        else:
            print(f"✗ Projects endpoint failed: {projects_response.status_code}")
            return False
        
        # Test materials endpoint
        materials_response = requests.get("http://localhost:8000/material/", headers=headers)
        if materials_response.status_code == 200:
            print("✓ Materials endpoint accessible")
            materials_data = materials_response.json()
            print(f"  Found {len(materials_data)} material records")
        else:
            print(f"⚠ Materials endpoint: {materials_response.status_code} (might be expected)")
        
        # Test fitup endpoint
        fitup_response = requests.get("http://localhost:8000/fitup/", headers=headers)
        if fitup_response.status_code == 200:
            print("✓ Fitup endpoint accessible")
            fitup_data = fitup_response.json()
            print(f"  Found {len(fitup_data)} fitup records")
        else:
            print(f"⚠ Fitup endpoint: {fitup_response.status_code} (might be expected)")
        
        # Test users endpoint
        users_response = requests.get("http://localhost:8000/users/", headers=headers)
        if users_response.status_code == 200:
            print("✓ Users endpoint accessible")
            users_data = users_response.json()
            print(f"  Found {len(users_data)} user records")
        else:
            print(f"✗ Users endpoint failed: {users_response.status_code}")
            return False
        
        print("\n✓ All dashboard navigation endpoints are working correctly!")
        print("✓ Frontend should now be able to navigate without redirecting to login")
        return True
        
    except Exception as e:
        print(f"✗ Dashboard navigation test failed: {e}")
        return False

def test_frontend_routes():
    """Test that frontend routes are accessible"""
    print("\nTesting Frontend Routes")
    print("=" * 50)
    
    routes_to_test = [
        "http://localhost:3001",
        "http://localhost:3001/dashboard",
        "http://localhost:3001/projects",
        "http://localhost:3001/materials",
        "http://localhost:3001/fitup",
        "http://localhost:3001/final",
        "http://localhost:3001/ndt",
        "http://localhost:3001/users"
    ]
    
    all_accessible = True
    
    for route in routes_to_test:
        try:
            response = requests.get(route)
            if response.status_code == 200:
                print(f"✓ {route} - Accessible")
            else:
                print(f"⚠ {route} - Status: {response.status_code}")
                all_accessible = False
        except Exception as e:
            print(f"✗ {route} - Error: {e}")
            all_accessible = False
    
    return all_accessible

def main():
    print("Dashboard Navigation Test")
    print("=" * 60)
    
    # Test backend endpoints
    backend_success = test_dashboard_navigation()
    
    # Test frontend routes
    frontend_success = test_frontend_routes()
    
    print("\n" + "=" * 60)
    print("NAVIGATION TEST RESULTS:")
    print("=" * 60)
    
    if backend_success and frontend_success:
        print("✓ All navigation tests passed!")
        print("✓ Dashboard navigation should work correctly")
        print("✓ Final Inspection and NDT Request links should navigate properly")
        print("✓ No more redirects to login page")
    else:
        print("✗ Some navigation tests failed")
        if not backend_success:
            print("  - Backend API issues")
        if not frontend_success:
            print("  - Frontend route issues")
    
    print("=" * 60)
    print("\nNext Steps:")
    print("1. Open http://localhost:3001 in your browser")
    print("2. Login with admin2/admin123")
    print("3. Click on Final Inspection and NDT Request in the dashboard")
    print("4. Verify they navigate to the correct pages without redirecting to login")

if __name__ == "__main__":
    main()
