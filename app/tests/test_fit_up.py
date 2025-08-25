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

# Test creating a fit-up inspection record
def test_create_fit_up_inspection():
    response = client.post(
        "/fit-ups/fit_up_inspections/",
        json={
            "drawing_no": "TEST-DRAWING",
            "system_spec": "TEST-SPEC",
            "line_no": "TEST-LINE",
            "spool_no": "TEST-SPOOL",
            "joint_no": "TEST-JOINT",
            "weld_type": "TEST-TYPE",
            "part1_unique_piece_id": "TEST-001",
            "part2_unique_piece_id": "TEST-002",
            "inspection_result": "PASS",
            "inspection_date": "2025-01-01",
            "inspection_operator": "TEST-OPERATOR",
            "inspection_remark": "TEST-REMARK"
        },
    )
    assert response.status_code == 201
    assert response.json()["drawing_no"] == "TEST-DRAWING"

# Test reading a fit-up inspection record
def test_read_fit_up_inspection():
    response = client.get(
        "/fit-ups/fit_up_inspections/1"
    )
    assert response.status_code == 200
    assert response.json()["drawing_no"] == "TEST-DRAWING"

# Test updating a fit-up inspection record
def test_update_fit_up_inspection():
    response = client.put(
        "/fit-ups/fit_up_inspections/1",
        json={
            "drawing_no": "UPDATED-DRAWING",
            "system_spec": "UPDATED-SPEC",
            "line_no": "UPDATED-LINE",
            "spool_no": "UPDATED-SPOOL",
            "joint_no": "UPDATED-JOINT",
            "weld_type": "UPDATED-TYPE",
            "part1_unique_piece_id": "UPDATED-001",
            "part2_unique_piece_id": "UPDATED-002",
            "inspection_result": "FAIL",
            "inspection_date": "2025-02-01",
            "inspection_operator": "UPDATED-OPERATOR",
            "inspection_remark": "UPDATED-REMARK"
        },
    )
    assert response.status_code == 200
    assert response.json()["drawing_no"] == "UPDATED-DRAWING"

# Test deleting a fit-up inspection record
def test_delete_fit_up_inspection():
    response = client.delete(
        "/fit-ups/fit_up_inspections/1"
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "Fit-up inspection deleted successfully"
