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

# Test creating a final inspection record
def test_create_final_inspection():
    response = client.post(
        "/finals/final_inspections/",
        json={
            "drawing_no": "TEST-DRAWING",
            "system_spec": "TEST-SPEC",
            "line_no": "TEST-LINE",
            "spool_no": "TEST-SPOOL",
            "joint_no": "TEST-JOINT",
            "weld_type": "TEST-TYPE",
            "wps_no": "TEST-WPS",
            "welder_no": "TEST-WELDER",
            "inspection_date": "2025-01-01",
            "final_report_no": "TEST-REPORT",
            "ndt_rt": "TEST-RT",
            "ndt_pt": "TEST-PT",
            "ndt_mt": "TEST-MT"
        },
    )
    assert response.status_code == 201
    assert response.json()["drawing_no"] == "TEST-DRAWING"

# Test reading a final inspection record
def test_read_final_inspection():
    response = client.get(
        "/finals/final_inspections/1"
    )
    assert response.status_code == 200
    assert response.json()["drawing_no"] == "TEST-DRAWING"

# Test updating a final inspection record
def test_update_final_inspection():
    response = client.put(
        "/finals/final_inspections/1",
        json={
            "drawing_no": "UPDATED-DRAWING",
            "system_spec": "UPDATED-SPEC",
            "line_no": "UPDATED-LINE",
            "spool_no": "UPDATED-SPOOL",
            "joint_no": "UPDATED-JOINT",
            "weld_type": "UPDATED-TYPE",
            "wps_no": "UPDATED-WPS",
            "welder_no": "UPDATED-WELDER",
            "inspection_date": "2025-02-01",
            "final_report_no": "UPDATED-REPORT",
            "ndt_rt": "UPDATED-RT",
            "ndt_pt": "UPDATED-PT",
            "ndt_mt": "UPDATED-MT"
        },
    )
    assert response.status_code == 200
    assert response.json()["drawing_no"] == "UPDATED-DRAWING"

# Test deleting a final inspection record
def test_delete_final_inspection():
    response = client.delete(
        "/finals/final_inspections/1"
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Final inspection deleted successfully"
