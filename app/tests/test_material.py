import sys
from fastapi.testclient import TestClient
from fastapi import FastAPI
sys.path.insert(0, 'D:/Backup/D_drive/deepseek_project/data_project') # Add the root directory to sys.path
from app.main import app

client = TestClient(app)

def override_get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Test creating a material inspection record
def test_create_material_inspection():
    response = client.post(
        "/materials/material_inspections/",
        json={
            "type_of_material": "Test Type",
            "material_grade": "Test Grade",
            "thickness": 10.5,
            "dia_for_pipe": 20.3,
            "heat_no": "Test Heat",
            "mvr_report_no": "Test MVR",
            "unique_piece_id": "TEST-001"
        },
    )
    assert response.status_code == 201
    assert response.json()["type_of_material"] == "Test Type"

# Test reading a material inspection record
def test_read_material_inspection():
    response = client.get(
        "/materials/material_inspections/1"
    )
    assert response.status_code == 200
    assert response.json()["type_of_material"] == "Test Type"

# Test updating a material inspection record
def test_update_material_inspection():
    response = client.put(
        "/materials/material_inspections/1",
        json={
            "type_of_material": "Updated Type",
            "material_grade": "Updated Grade",
            "thickness": 11.5,
            "dia_for_pipe": 21.3,
            "heat_no": "Updated Heat",
            "mvr_report_no": "Updated MVR",
            "unique_piece_id": "TEST-001"
        },
    )
    assert response.status_code == 200
    assert response.json()["type_of_material"] == "Updated Type"

# Test deleting a material inspection record
def test_delete_material_inspection():
    response = client.delete(
        "/materials/material_inspections/1"
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Material inspection deleted successfully"
