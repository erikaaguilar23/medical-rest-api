import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_get_doctors(client):
    resp = client.get("/doctors")
    assert resp.status_code == 200

def test_get_doctors_xml(client):
    resp = client.get("/doctors?format=xml")
    assert resp.status_code == 200
    assert resp.headers["Content-Type"] == "application/xml"
