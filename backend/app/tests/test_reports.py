from datetime import datetime, timedelta, UTC


def test_income_statement_basic(client):
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

    # Income transaction: +1000 asset / -1000 income
    client.post("/transactions", json={
        "description": "Paycheck",
        "entries": [
            {"account_id": checking, "amount": 100000},
            {"account_id": income, "amount": -100000}
        ]
    })

    # Expense transaction: -200 asset / +200 expense
    client.post("/transactions", json={
        "description": "Groceries",
        "entries": [
            {"account_id": checking, "amount": -20000},
            {"account_id": expense, "amount": 20000}
        ]
    })

    report = client.get("/reports/income-statement").json()

    assert report["income"] == 100000
    assert report["expenses"] == 20000
    assert report["net_income"] == 80000


def test_balance_sheet_basic(client):
    checking = client.post("/accounts", json={
        "name": "Checking",
        "type": "asset"
    }).json()["id"]

    credit = client.post("/accounts", json={
        "name": "Credit Card",
        "type": "liability"
    }).json()["id"]

    # Borrow 500
    client.post("/transactions", json={
        "description": "Borrow",
        "entries": [
            {"account_id": checking, "amount": 50000},
            {"account_id": credit, "amount": -50000}
        ]
    })

    sheet = client.get("/reports/balance-sheet").json()

    assert sheet["assets"] == 50000
    assert sheet["liabilities"] == 50000
    assert sheet["equity"] == 0


def test_income_statement_date_filter(client):
    checking = client.post("/accounts", json={
        "name": "Checking",
        "type": "asset"
    }).json()["id"]

    income = client.post("/accounts", json={
        "name": "Salary",
        "type": "income"
    }).json()["id"]

    # Old transaction (simulate by updating date manually if needed)
    client.post("/transactions", json={
        "description": "Old income",
        "entries": [
            {"account_id": checking, "amount": 100000},
            {"account_id": income, "amount": -100000}
        ]
    })

    future_start = datetime.now(UTC) + timedelta(days=1)

    response = client.get(
        "/reports/income-statement",
        params={"start_date": future_start.isoformat()}
    )

    assert response.status_code == 200

    report = response.json()

    assert report["income"] == 0
    assert report["expenses"] == 0
    assert report["net_income"] == 0