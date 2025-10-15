import requests
import json
from datetime import date

# Test configuration
BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/token"
PROJECTS_ENDPOINT = f"{BASE_URL}/projects/"

# Test credentials
admin_credentials = {
    "username": "admin2",
    "password": "admin123"
}

# Test project data - simplified
test_project = {
    "project_number": "PROJ-001",
    "project_name": "Test Fabrication Project",
    "client": "Test Client Inc.",
    "start_date": str(date.today()),
    "status": "active",
    "project_manager": "John Doe"
}

def debug_project_creation():
    print("🔍 Debugging Project Creation")
    print("=" * 50)
    
    # Step 1: Login as admin
    print("1. Logging in as admin...")
    try:
        response = requests.post(LOGIN_ENDPOINT, data=admin_credentials)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login successful")
            print(f"   Token: {token[:20]}...")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 2: Test GET projects first
    print("\n2. Testing GET projects endpoint...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.get(PROJECTS_ENDPOINT, headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ GET projects successful - {len(projects)} projects")
        else:
            print(f"❌ GET projects failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ GET projects error: {e}")
    
    # Step 3: Create a new project with detailed error info
    print("\n3. Creating a new project...")
    try:
        print(f"   Sending data: {json.dumps(test_project, indent=2)}")
        response = requests.post(PROJECTS_ENDPOINT, json=test_project, headers=headers)
        print(f"   Response status: {response.status_code}")
        print(f"   Response headers: {dict(response.headers)}")
        if response.status_code == 200:
            created_project = response.json()
            print("✅ Project created successfully!")
            print(f"   Project ID: {created_project['id']}")
            print(f"   Project Number: {created_project['project_number']}")
        else:
            print(f"❌ Project creation failed: {response.status_code}")
            print(f"   Response text: {response.text}")
            # Try to get more detailed error info
            try:
                error_detail = response.json()
                print(f"   Error detail: {error_detail}")
            except:
                print(f"   Raw error: {response.text}")
    except Exception as e:
        print(f"❌ Project creation error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_project_creation()
