def test_summary_correct_totals(client):
    client.post("/api/categories/", json={"name": "Food"})
    client.post("/api/categories/", json={"name": "Transport"})
    client.post("/api/transactions/", json={"description": "Lunch", "amount": 20.0, "date": "2026-02-21", "category_id": 1})
    client.post("/api/transactions/", json={"description": "Dinner", "amount": 30.0, "date": "2026-02-21", "category_id": 1})
    client.post("/api/transactions/", json={"description": "Bus", "amount": 10.0, "date": "2026-02-21", "category_id": 2})

    res = client.get("/api/summary/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["overall_total"] == 60.0

    food = next(r for r in data["breakdown"] if r["category_name"] == "Food")
    assert food["total_spent"] == 50.0
    assert food["transaction_count"] == 2


def test_summary_excludes_deleted_transactions(client):
    client.post("/api/categories/", json={"name": "Food"})
    client.post("/api/transactions/", json={"description": "Lunch", "amount": 20.0, "date": "2026-02-21", "category_id": 1})
    client.post("/api/transactions/", json={"description": "Dinner", "amount": 30.0, "date": "2026-02-21", "category_id": 1})
    client.delete("/api/transactions/1")

    res = client.get("/api/summary/")
    data = res.get_json()
    assert data["overall_total"] == 30.0


def test_summary_empty(client):
    res = client.get("/api/summary/")
    assert res.status_code == 200
    data = res.get_json()
    assert data["overall_total"] == 0.0
    assert data["breakdown"] == []