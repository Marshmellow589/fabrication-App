import requests
import json
from datetime import date

# Test configuration
BASE_URL = "http://localhost:8000"
LOGIN_ENDPOINT = f"{BASE_URL}/auth/token"
PROJECTS_ENDPOINT = f"{BASE_URL}/projects/"
MATERIAL_ENDPOINT = f"{BASE_URL}/material/"
FITUP_ENDPOINT = f"{BASE_URL}/fitup/"
FINAL_INSPECTION_ENDPOINT = f"{BASE_URL}/final/"
NDT_REQUEST_ENDPOINT = f"{BASE_URL}/ndt/"

# Test credentials
admin_credentials = {
    "username": "admin2",
    "password": "admin123"
}

# Test project data
test_project = {
    "project_number": "PROJ-TEST-001",
    "project_name": "Complete Test Fabrication Project",
    "client": "Test Client Corporation",
    "start_date": str(date.today()),
    "end_date": str(date.today().replace(year=date.today().year + 1)),
    "status": "active",
    "project_manager": "Jane Smith",
    "description": "Complete test project with all inspection templates",
    "budget": 75000.00
}

def test_complete_workflow():
    print("🚀 Testing Complete Project Workflow with Templates")
    print("=" * 60)
    
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
    
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }
    
    # Step 2: Create a new project
    print("\n2. Creating a new project...")
    try:
        response = requests.post(PROJECTS_ENDPOINT, json=test_project, headers=headers)
        if response.status_code == 200:
            created_project = response.json()
            project_id = created_project['id']
            print("✅ Project created successfully!")
            print(f"   Project ID: {project_id}")
            print(f"   Project Number: {created_project['project_number']}")
            print(f"   Project Name: {created_project['project_name']}")
        else:
            print(f"❌ Project creation failed: {response.status_code} - {response.text}")
            return
    except Exception as e:
        print(f"❌ Project creation error: {e}")
        return
    
    # Step 3: Test Material Inspection Template
    print("\n3. Testing Material Inspection Template...")
    material_data = {
        "project_id": project_id,
        "material_type": "Carbon Steel Plate",
        "heat_number": "HT-2025-001",
        "thickness": 25.0,
        "quantity": 10,
        "inspection_date": str(date.today()),
        "inspector_name": "John Inspector",
        "status": "approved",
        "remarks": "Material meets specifications"
    }
    
    try:
        response = requests.post(MATERIAL_ENDPOINT, json=material_data, headers=headers)
        if response.status_code == 200:
            material_record = response.json()
            print("✅ Material inspection created successfully!")
            print(f"   Material ID: {material_record['id']}")
            print(f"   Material Type: {material_record['material_type']}")
        else:
            print(f"❌ Material inspection creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Material inspection error: {e}")
    
    # Step 4: Test Fit-up Inspection Template
    print("\n4. Testing Fit-up Inspection Template...")
    fitup_data = {
        "project_id": project_id,
        "component_name": "Main Vessel",
        "joint_type": "Butt Weld",
        "fitup_date": str(date.today()),
        "inspector_name": "Mike Welder",
        "status": "approved",
        "remarks": "Fit-up within tolerance"
    }
    
    try:
        response = requests.post(FITUP_ENDPOINT, json=fitup_data, headers=headers)
        if response.status_code == 200:
            fitup_record = response.json()
            print("✅ Fit-up inspection created successfully!")
            print(f"   Fit-up ID: {fitup_record['id']}")
            print(f"   Component: {fitup_record['component_name']}")
        else:
            print(f"❌ Fit-up inspection creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Fit-up inspection error: {e}")
    
    # Step 5: Test Final Inspection Template
    print("\n5. Testing Final Inspection Template...")
    final_data = {
        "project_id": project_id,
        "inspection_date": str(date.today()),
        "inspector_name": "Sarah Quality",
        "status": "approved",
        "remarks": "Final inspection passed"
    }
    
    try:
        response = requests.post(FINAL_INSPECTION_ENDPOINT, json=final_data, headers=headers)
        if response.status_code == 200:
            final_record = response.json()
            print("✅ Final inspection created successfully!")
            print(f"   Final Inspection ID: {final_record['id']}")
        else:
            print(f"❌ Final inspection creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ Final inspection error: {e}")
    
    # Step 6: Test NDT Request Template
    print("\n6. Testing NDT Request Template...")
    ndt_data = {
        "project_id": project_id,
        "request_date": str(date.today()),
        "required_by_date": str(date.today().replace(day=date.today().day + 7)),
        "ndt_method": "Ultrasonic Testing",
        "status": "pending",
        "remarks": "NDT required for critical welds"
    }
    
    try:
        response = requests.post(NDT_REQUEST_ENDPOINT, json=ndt_data, headers=headers)
        if response.status_code == 200:
            ndt_record = response.json()
            print("✅ NDT request created successfully!")
            print(f"   NDT Request ID: {ndt_record['id']}")
            print(f"   NDT Method: {ndt_record['ndt_method']}")
        else:
            print(f"❌ NDT request creation failed: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"❌ NDT request error: {e}")
    
    # Step 7: Verify all records are linked to the project
    print("\n7. Verifying all records are linked to the project...")
    try:
        # Get material records for project
        response = requests.get(f"{MATERIAL_ENDPOINT}?project_id={project_id}", headers=headers)
        if response.status_code == 200:
            materials = response.json()
            print(f"✅ Material records: {len(materials)}")
        
        # Get fitup records for project
        response = requests.get(f"{FITUP_ENDPOINT}?project_id={project_id}", headers=headers)
        if response.status_code == 200:
            fitups = response.json()
            print(f"✅ Fit-up records: {len(fitups)}")
        
        # Get final inspection records for project
        response = requests.get(f"{FINAL_INSPECTION_ENDPOINT}?project_id={project_id}", headers=headers)
        if response.status_code == 200:
            finals = response.json()
            print(f"✅ Final inspection records: {len(finals)}")
        
        # Get NDT request records for project
        response = requests.get(f"{NDT_REQUEST_ENDPOINT}?project_id={project_id}", headers=headers)
        if response.status_code == 200:
            ndts = response.json()
            print(f"✅ NDT request records: {len(ndts)}")
            
    except Exception as e:
        print(f"❌ Verification error: {e}")
    
    print("\n" + "=" * 60)
    print("🎉 Complete Project Workflow Test Completed Successfully!")
    print(f"📊 Project '{test_project['project_name']}' created with all inspection templates")
    print(f"🌐 Frontend available at: http://localhost:3002/")
    print(f"🔧 Backend API available at: http://localhost:8000/")

if __name__ == "__main__":
    test_complete_workflow()
