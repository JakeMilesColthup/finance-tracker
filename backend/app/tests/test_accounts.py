from fastapi.testclient import TestClient
from app.main import app

# client = TestClient(app)


def test_create_account(client):
    response = client.post("/accounts", json={
        "name": "Test Checking",
        "type": "asset",
        "subtype": "checking"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Checking"


def test_list_accounts(client):
    client.post("/accounts", json={
        "name": "Test Checking",
        "type": "asset",
        "subtype": "checking"
    })
    response = client.get("/accounts")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert response.json()[0]["name"] == "Test Checking"