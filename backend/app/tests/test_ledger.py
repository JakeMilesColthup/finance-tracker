def test_create_balanced_transaction(client):
    # create two accounts first
    client.post("/accounts", json={"name": "Cash", "type": "asset"})
    client.post("/accounts", json={"name": "Income", "type": "income"})

    response = client.post("/transactions", json={
        "description": "Test",
        "entries": [
            {"account_id": 1, "amount": 10000},
            {"account_id": 2, "amount": -10000}
        ]
    })

    assert response.status_code == 200
    data = response.json()
    assert data["description"] == "Test"
    assert len(data["entries"]) == 2


def test_reject_imbalanced_transaction(client):
    # create accounts first
    client.post("/accounts", json={"name": "Cash", "type": "asset"})
    client.post("/accounts", json={"name": "Income", "type": "income"})

    response = client.post("/transactions", json={
        "description": "Bad",
        "entries": [
            {"account_id": 1, "amount": 10000},
            {"account_id": 2, "amount": -9000}
        ]
    })

    assert response.status_code == 400