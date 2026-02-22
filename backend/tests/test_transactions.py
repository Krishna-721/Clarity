def test_create_transaction(client):
    client.post("/api/categories/", json={"name": "Food"})
    res = client.post("/api/transactions/", json={
        "description": "Lunch",
        "amount": 12.50,
        "date": "2026-02-21",
        "category_id": 1
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["amount"] == 12.50
    assert data["category"]["name"] == "Food"


def test_create_transaction_negative_amount(client):
    client.post("/api/categories/", json={"name": "Food"})
    res = client.post("/api/transactions/", json={
        "description": "Bad",
        "amount": -5.0,
        "date": "2026-02-21",
        "category_id": 1
    })
    assert res.status_code == 400


def test_create_transaction_zero_amount(client):
    client.post("/api/categories/", json={"name": "Food"})
    res = client.post("/api/transactions/", json={
        "description": "Zero",
        "amount": 0,
        "date": "2026-02-21",
        "category_id": 1
    })
    assert res.status_code == 400


def test_create_transaction_invalid_category(client):
    res = client.post("/api/transactions/", json={
        "description": "Lunch",
        "amount": 10.0,
        "date": "2026-02-21",
        "category_id": 999
    })
    assert res.status_code == 404


def test_create_transaction_deleted_category(client):
    client.post("/api/categories/", json={"name": "Food"})
    client.delete("/api/categories/1")
    res = client.post("/api/transactions/", json={
        "description": "Lunch",
        "amount": 10.0,
        "date": "2026-02-21",
        "category_id": 1
    })
    assert res.status_code == 404


def test_get_transactions_filter_by_category(client):
    client.post("/api/categories/", json={"name": "Food"})
    client.post("/api/categories/", json={"name": "Transport"})
    client.post("/api/transactions/", json={"description": "Lunch", "amount": 10.0, "date": "2026-02-21", "category_id": 1})
    client.post("/api/transactions/", json={"description": "Bus", "amount": 5.0, "date": "2026-02-21", "category_id": 2})
    res = client.get("/api/transactions/?category_id=1")
    data = res.get_json()
    assert len(data) == 1
    assert data[0]["description"] == "Lunch"


def test_delete_transaction(client):
    client.post("/api/categories/", json={"name": "Food"})
    client.post("/api/transactions/", json={"description": "Lunch", "amount": 10.0, "date": "2026-02-21", "category_id": 1})
    res = client.delete("/api/transactions/1")
    assert res.status_code == 200
    transactions = client.get("/api/transactions/").get_json()
    assert len(transactions) == 0