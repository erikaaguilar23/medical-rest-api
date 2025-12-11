import pytest
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_get_assignments(client):
    resp = client.get("/assignments")
    assert resp.status_code == 200
