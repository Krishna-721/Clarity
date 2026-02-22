import json


def test_create_category(client):
    res = client.post("/api/categories/", json={"name": "Food", "description": "Groceries"})
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == "Food"
    assert data["is_deleted"] == False


def test_create_category_duplicate_name(client):
    client.post("/api/categories/", json={"name": "Food"})
    res = client.post("/api/categories/", json={"name": "Food"})
    assert res.status_code == 409


def test_create_category_blank_name(client):
    res = client.post("/api/categories/", json={"name": "   "})
    assert res.status_code == 400


def test_create_category_missing_name(client):
    res = client.post("/api/categories/", json={"description": "No name given"})
    assert res.status_code == 400


def test_get_categories(client):
    client.post("/api/categories/", json={"name": "Food"})
    client.post("/api/categories/", json={"name": "Transport"})
    res = client.get("/api/categories/")
    assert res.status_code == 200
    assert len(res.get_json()) == 2


def test_delete_category_no_transactions(client):
    client.post("/api/categories/", json={"name": "Food"})
    res = client.delete("/api/categories/1")
    assert res.status_code == 200
    # confirm it no longer shows up in list
    categories = client.get("/api/categories/").get_json()
    assert len(categories) == 0


def test_delete_category_with_transactions(client):
    client.post("/api/categories/", json={"name": "Food"})
    client.post("/api/transactions/", json={
        "description": "Lunch",
        "amount": 10.0,
        "date": "2026-02-21",
        "category_id": 1
    })
    res = client.delete("/api/categories/1")
    assert res.status_code == 409


def test_delete_nonexistent_category(client):
    res = client.delete("/api/categories/999")
    assert res.status_code == 404