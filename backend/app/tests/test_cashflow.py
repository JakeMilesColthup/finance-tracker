from datetime import datetime, UTC


def test_monthly_cash_flow_basic(client):

    # Create accounts
    checking = client.post("/accounts", json={
        "name": "Checking",
        "type": "asset"
    }).json()["id"]

    income = client.post("/accounts", json={
        "name": "Salary",
        "type": "income"
    }).json()["id"]

    expense = client.post("/accounts", json={
        "name": "Food",
        "type": "expense"
    }).json()["id"]

    # January income
    client.post("/transactions", json={
        "description": "Jan salary",
        "entries": [
            {"account_id": checking, "amount": 100000},
            {"account_id": income, "amount": -100000}
        ]
    })

    # January expense
    client.post("/transactions", json={
        "description": "Groceries",
        "entries": [
            {"account_id": checking, "amount": -20000},
            {"account_id": expense, "amount": 20000}
        ]
    })

    year = datetime.now(UTC).year
    month = datetime.now(UTC).month

    response = client.get(
        "/cash-flow/",
        params={"year": year}
    )

    assert response.status_code == 200

    data = response.json()
    monthly = data[f"{year}-{month:02d}"]

    assert monthly["income"] == 100000
    assert monthly["expenses"] == 20000
    assert monthly["net"] == 80000


def test_internal_transfer_excluded(client):

    checking = client.post("/accounts", json={
        "name": "Checking",
        "type": "asset"
    }).json()["id"]

    savings = client.post("/accounts", json={
        "name": "Savings",
        "type": "asset"
    }).json()["id"]

    # Transfer between asset accounts
    client.post("/transactions", json={
        "description": "Transfer",
        "entries": [
            {"account_id": checking, "amount": -50000},
            {"account_id": savings, "amount": 50000}
        ]
    })

    year = datetime.now(UTC).year
    month = datetime.now(UTC).month

    response = client.get(
        "/cash-flow/",
        params={"year": year}
    )

    data = response.json()
    monthly = data[f"{year}-{month:02d}"]

    # Should not count as income or expense
    assert monthly["income"] == 0
    assert monthly["expenses"] == 0
    assert monthly["net"] == 0