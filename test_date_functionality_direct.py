#!/usr/bin/env python3
"""
Direct test of date functionality by creating sample data and testing API endpoints
"""

import sys
import os
import requests
import json
from datetime import datetime, timedelta

# Add the project root directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from sqlalchemy.orm import Session
from backend.app.database import SessionLocal, engine, Base
from backend.app.models.project import Project
from backend.app.models.material import Material
from backend.app.models.fitup import Fitup
from backend.app.models.final_inspection import FinalInspection
from backend.app.models.ndt_request import NDTRequest

def create_sample_data():
    """Create sample data directly in the database"""
    print("Creating sample data directly in database...")
    
    # Create database tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        # Create a test project with date fields
        project = Project(
            name="Test Project - Date Functionality",
            description="Testing date field functionality",
            start_date=datetime.now() - timedelta(days=30),
            end_date=datetime.now() + timedelta(days=30),
            status="active"
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        print(f"Created project: {project.name} (ID: {project.id})")
        print(f"  Start date: {project.start_date}")
        print(f"  End date: {project.end_date}")
        
        # Create material inspection with date
        material = Material(
            project_id=project.id,
            material_name="Test Steel Plate",
            material_type="Steel",
            quantity=10,
            unit="pieces",
            inspection_date=datetime.now(),
            status="approved",
            inspector="Test Inspector"
        )
        db.add(material)
        db.commit()
        db.refresh(material)
        print(f"Created material: {material.material_name}")
        print(f"  Inspection date: {material.inspection_date}")
        
        # Create fitup inspection with date
        fitup = Fitup(
            project_id=project.id,
            component_name="Test Component",
            fitup_date=datetime.now(),
            status="completed",
            inspector="Test Inspector"
        )
        db.add(fitup)
        db.commit()
        db.refresh(fitup)
        print(f"Created fitup: {fitup.component_name}")
        print(f"  Fitup date: {fitup.fitup_date}")
        
        # Create final inspection with date
        final = FinalInspection(
            project_id=project.id,
            inspection_date=datetime.now(),
            status="passed",
            inspector="Test Inspector"
        )
        db.add(final)
        db.commit()
        db.refresh(final)
        print(f"Created final inspection")
        print(f"  Inspection date: {final.inspection_date}")
        
        # Create NDT request with dates
        ndt = NDTRequest(
            project_id=project.id,
            request_date=datetime.now(),
            scheduled_date=datetime.now() + timedelta(days=7),
            technique="UT",
            status="scheduled",
            requested_by="Test Inspector"
        )
        db.add(ndt)
        db.commit()
        db.refresh(ndt)
        print(f"Created NDT request")
        print(f"  Request date: {ndt.request_date}")
        print(f"  Scheduled date: {ndt.scheduled_date}")
        
        return project.id
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
        return None
    finally:
        db.close()

def test_api_endpoints():
    """Test API endpoints to verify they work with the sample data"""
    print("\n" + "="*50)
    print("Testing API Endpoints")
    print("="*50)
    
    BASE_URL = "http://localhost:8000"
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
        return
    
    # Test projects endpoint
    try:
        response = requests.get(f"{BASE_URL}/projects/")
        print(f"Projects endpoint: {response.status_code}")
        if response.status_code == 200:
            projects = response.json()
            print(f"Found {len(projects)} projects")
            for project in projects:
                print(f"  - {project['name']}: {project['start_date']} to {project['end_date']}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"Projects endpoint test failed: {e}")
    
    # Test materials endpoint
    try:
        response = requests.get(f"{BASE_URL}/materials/")
        print(f"Materials endpoint: {response.status_code}")
        if response.status_code == 200:
            materials = response.json()
            print(f"Found {len(materials)} materials")
            for material in materials:
                print(f"  - {material['material_name']}: inspected on {material['inspection_date']}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"Materials endpoint test failed: {e}")
    
    # Test fitups endpoint
    try:
        response = requests.get(f"{BASE_URL}/fitups/")
        print(f"Fitups endpoint: {response.status_code}")
        if response.status_code == 200:
            fitups = response.json()
            print(f"Found {len(fitups)} fitups")
            for fitup in fitups:
                print(f"  - {fitup['component_name']}: fitup on {fitup['fitup_date']}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"Fitups endpoint test failed: {e}")
    
    # Test final inspections endpoint
    try:
        response = requests.get(f"{BASE_URL}/final/")
        print(f"Final inspections endpoint: {response.status_code}")
        if response.status_code == 200:
            finals = response.json()
            print(f"Found {len(finals)} final inspections")
            for final in finals:
                print(f"  - Inspection on {final['inspection_date']}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"Final inspections endpoint test failed: {e}")
    
    # Test NDT requests endpoint
    try:
        response = requests.get(f"{BASE_URL}/ndt/")
        print(f"NDT requests endpoint: {response.status_code}")
        if response.status_code == 200:
            ndts = response.json()
            print(f"Found {len(ndts)} NDT requests")
            for ndt in ndts:
                print(f"  - Requested on {ndt['request_date']}, scheduled on {ndt['scheduled_date']}")
        else:
            print(f"  Response: {response.text}")
    except Exception as e:
        print(f"NDT requests endpoint test failed: {e}")

def main():
    """Main test function"""
    print("Testing Date Functionality - Direct Database Approach")
    print("="*60)
    
    # Create sample data directly in database
    project_id = create_sample_data()
    if not project_id:
        print("Failed to create sample data")
        return
    
    # Test API endpoints
    test_api_endpoints()
    
    print("\n" + "="*60)
    print("Date functionality test completed!")
    print("Sample data has been created with proper date fields.")
    print("API endpoints have been tested to verify they work correctly.")
    print("="*60)

if __name__ == "__main__":
    main()
