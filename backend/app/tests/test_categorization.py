def test_categorization_rule(client):

    checking = client.post("/accounts", json={
        "name": "Checking",
        "type": "asset"
    }).json()["id"]

    # root expense category
    expenses = client.post("/accounts", json={
        "name": "Expenses",
        "type": "expense"
    }).json()["id"]

    groceries = client.post("/accounts", json={
        "name": "Groceries",
        "type": "expense",
        "parent_id": expenses
    }).json()["id"]

    client.post("/accounts", json={
        "name": "Income",
        "type": "income"
    })

    client.post("/category_rules", json={
        "pattern": "COSTCO",
        "match_type": "contains",
        "account_id": groceries
    })

    csv_content = """date,description,amount
2026-01-01,COSTCO WHOLESALE,-100
"""

    response = client.post(
        f"/ingestion/csv/{checking}",
        files={"file": ("statement.csv", csv_content)},
    )

    assert response.status_code == 200
    assert response.json()["imported"] == 1

    balances = client.get("/balances/").json()

    groceries_balance = next(
        a["balance"] for a in balances if a["name"] == "Groceries"
    )

    assert groceries_balance == 100