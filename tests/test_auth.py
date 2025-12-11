import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_login_success(client):
    response = client.post("/login", json={"username": "admin", "password": "1234"})
    assert response.status_code == 200
    json_data = response.get_json()
    assert "token" in json_data

def test_login_fail(client):
    response = client.post("/login", json={"username": "wrong", "password": "wrong"})
    assert response.status_code == 401
