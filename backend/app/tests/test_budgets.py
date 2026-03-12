def test_budget_vs_actual(client):

    checking = client.post("/accounts", json={
        "name": "Checking",
        "type": "asset"
    }).json()["id"]

    groceries = client.post("/accounts", json={
        "name": "Groceries",
        "type": "expense"
    }).json()["id"]

    client.post("/accounts", json={
        "name": "Income",
        "type": "income"
    })

    client.post("/transactions", json={
        "description": "Groceries",
        "entries": [
            {"account_id": checking, "amount": -500},
            {"account_id": groceries, "amount": 500}
        ],
        "created_at": "2026-01-15T12:00:00"   # <-- match budget range
    })

    budget = client.post("/budgets", json={
        "start_date": "2026-01-01",
        "end_date": "2026-01-31",
        "items": [
            {"account_id": groceries, "amount": 1000}
        ]
    }).json()

    status = client.get(f"/budgets/{budget['budget_id']}/status").json()

    assert status[0]["actual"] == 500
    assert status[0]["remaining"] == 500