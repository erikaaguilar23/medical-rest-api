import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_get_patients_json(client):
    resp = client.get("/patients?format=json")
    assert resp.status_code == 200

def test_get_patients_xml(client):
    resp = client.get("/patients?format=xml")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/xml"
