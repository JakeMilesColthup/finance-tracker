from app.models.account import AccountType

def test_account_balance_calculation(client):
    # Create accounts
    checking = client.post("/accounts", json={"name": "Checking", "type": "asset"}).json()["id"]
    income = client.post("/accounts", json={"name": "Income", "type": "income"}).json()["id"]

    # Add a transaction: +1000 to checking, -1000 to income
    client.post("/transactions", json={
        "description": "Paycheck",
        "entries": [
            {"account_id": checking, "amount": 100000},
            {"account_id": income, "amount": -100000}
        ]
    })

    # Fetch balances
    balances = client.get("/balances/").json()
    checking_balance = next(b for b in balances if b["account_id"] == checking)

    assert checking_balance["balance"] == 100000


def test_net_worth_calculation(client):
    # Create asset and liability
    checking = client.post("/accounts", json={"name": "Checking", "type": "asset"}).json()["id"]
    credit = client.post("/accounts", json={"name": "Credit Card", "type": "liability"}).json()["id"]

    # Borrow $500: checking +500, credit liability +500
    client.post("/transactions", json={
        "description": "Borrow",
        "entries": [
            {"account_id": checking, "amount": 50000},
            {"account_id": credit, "amount": -50000}
        ]
    })

    # Net worth should be zero: 50000 asset - 50000 liability
    net_worth = client.get("/balances/net-worth").json()["net_worth"]
    assert net_worth == 0