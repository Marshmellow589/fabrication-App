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

# Test user registration
def test_register_user():
    response = client.post(
        "/users/register",
        json={
            "email": "test@example.com",
            "username": "testuser",
            "full_name": "Test User",
            "password": "testpass",
            "role": "inspector"
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

# Test user login
def test_login_user():
    response = client.post(
        "/users/login",
        json={"username": "testuser", "password": "testpass"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()

# Test password reset
def test_password_reset():
    response = client.post(
        "/users/password_reset",
        json={"username": "testuser", "password": "newpassword"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
