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

# Test creating an NDT request record
def test_create_ndt_request():
    response = client.post(
        "/ndts/ndt_requests/",
        json={
            "line_no": "TEST-LINE",
            "spool_no": "TEST-SPOOL",
            "joint_no": "TEST-JOINT",
            "weld_type": "TEST-TYPE",
            "thickness": 10.5,
            "dia": 20.3,
            "weld_no": "TEST-WELD",
            "weld_process": "TEST-PROCESS",
            "ndt_rt_remark": "TEST-RT-REMARK",
            "ndt_pt_remark": "TEST-PT-REMARK",
            "ndt_mt_remark": "TEST-MT-REMARK",
            "ndt_rfi_date": "2025-01-01",
            "rfi_no": "TEST-RFI"
        },
    )
    assert response.status_code == 201
    assert response.json()["line_no"] == "TEST-LINE"

# Test reading an NDT request record
def test_read_ndt_request():
    response = client.get(
        "/ndts/ndt_requests/1"
    )
    assert response.status_code == 200
    assert response.json()["line_no"] == "TEST-LINE"

# Test updating an NDT request record
def test_update_ndt_request():
    response = client.put(
        "/ndts/ndt_requests/1",
        json={
            "line_no": "UPDATED-LINE",
            "spool_no": "UPDATED-SPOOL",
            "joint_no": "UPDATED-JOINT",
            "weld_type": "UPDATED-TYPE",
            "thickness": 11.5,
            "dia": 21.3,
            "weld_no": "UPDATED-WELD",
            "weld_process": "UPDATED-PROCESS",
            "ndt_rt_remark": "UPDATED-RT-REMARK",
            "ndt_pt_remark": "UPDATED-PT-REMARK",
            "ndt_mt_remark": "UPDATED-MT-REMARK",
            "ndt_rfi_date": "2025-02-01",
            "rfi_no": "UPDATED-RFI"
        },
    )
    assert response.status_code == 200
    assert response.json()["line_no"] == "UPDATED-LINE"

# Test deleting an NDT request record
def test_delete_ndt_request():
    response = client.delete(
        "/ndts/ndt_requests/1"
    )
    assert response.status_code == 200
    assert response.json()["detail"] == "NDT request deleted successfully"
