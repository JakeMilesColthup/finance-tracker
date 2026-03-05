def test_csv_ingestion(client):

    # Create accounts
    checking = client.post("/accounts", json={
        "name": "Checking",
        "type": "asset"
    }).json()["id"]

    client.post("/accounts", json={
        "name": "Income",
        "type": "income"
    })

    client.post("/accounts", json={
        "name": "Expenses",
        "type": "expense"
    })

    csv_content = """date,description,amount
2026-01-01,Salary,1000
2026-01-02,Groceries,-200
"""

    response = client.post(
        f"/ingestion/csv/{checking}",
        files={"file": ("statement.csv", csv_content)},
    )

    assert response.status_code == 200
    assert response.json()["imported"] == 2

    balances = client.get("/balances/").json()

    # Checking: +1000 - 200 = 800
    checking_balance = next(
        a["balance"] for a in balances if a["name"] == "Checking"
    )

    assert checking_balance == 800