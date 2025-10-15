import requests
import json
from datetime import datetime, date

# Test configuration
BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/token"
PROJECTS_ENDPOINT = f"{BASE_URL}/projects/"

# Test credentials
admin_credentials = {
    "username": "admin2",
    "password": "admin123"
}

# Test project data
test_project = {
    "project_number": "PROJ-001",
    "project_name": "Test Fabrication Project",
    "client": "Test Client Inc.",
    "start_date": str(date.today()),
    "end_date": str(date.today().replace(year=date.today().year + 1)),
    "status": "active",
    "project_manager": "John Doe",
    "description": "This is a test fabrication project",
    "budget": 50000.00
}

def test_project_creation():
    print("🧪 Testing Project Creation Functionality")
    print("=" * 50)
    
    # Step 1: Login as admin
    print("1. Logging in as admin...")
    try:
        response = requests.post(LOGIN_ENDPOINT, data=admin_credentials)
        if response.status_code == 200:
            token = response.json()["access_token"]
            print("✅ Login successful")
        else:
            print(f"❌ Login failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Login error: {e}")
        return
    
    # Step 2: Create a new project
    print("\n2. Creating a new project...")
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(PROJECTS_ENDPOINT, json=test_project, headers=headers)
        if response.status_code == 200:
            created_project = response.json()
            print("✅ Project created successfully!")
            print(f"   Project ID: {created_project['id']}")
            print(f"   Project Number: {created_project['project_number']}")
            print(f"   Project Name: {created_project['project_name']}")
            print(f"   Client: {created_project['client']}")
            print(f"   Status: {created_project['status']}")
        else:
            print(f"❌ Project creation failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Project creation error: {e}")
        return
    
    # Step 3: Retrieve all projects to verify
    print("\n3. Retrieving all projects to verify...")
    try:
        response = requests.get(PROJECTS_ENDPOINT, headers=headers)
        if response.status_code == 200:
            projects = response.json()
            print(f"✅ Retrieved {len(projects)} projects")
            if projects:
                print("Latest projects:")
                for project in projects[-3:]:  # Show last 3 projects
                    print(f"   - {project['project_number']}: {project['project_name']} ({project['status']})")
        else:
            print(f"❌ Failed to retrieve projects: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Project retrieval error: {e}")
    
    # Step 4: Test duplicate project number
    print("\n4. Testing duplicate project number protection...")
    try:
        response = requests.post(PROJECTS_ENDPOINT, json=test_project, headers=headers)
        if response.status_code == 400:
            print("✅ Duplicate project number protection working correctly")
            print(f"   Error message: {response.json()['detail']}")
        else:
            print(f"❌ Expected 400 error but got: {response.status_code}")
    except Exception as e:
        print(f"❌ Duplicate test error: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Project Creation Test Completed!")

if __name__ == "__main__":
    test_project_creation()
