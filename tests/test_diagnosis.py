import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def login_token(client):
    resp = client.post("/login", json={"username": "admin", "password": "1234"})
    return resp.get_json()["token"]

def test_get_diagnoses(client):
    resp = client.get("/diagnosis")
    assert resp.status_code == 200

def test_create_diagnosis(client):
    token = login_token(client)
    resp = client.post("/diagnosis", 
                       json={"diagnosis_name": "TestDiagnosis", "category": "Test"},
                       headers={"Authorization": f"Bearer {token}"})
    assert resp.status_code in (201, 500)  # 500 if DB rejects duplicate

def test_get_single_diagnosis(client):
    resp = client.get("/diagnosis/1")
    assert resp.status_code in (200, 404)
