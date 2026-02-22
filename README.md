# Clarity - Know Your Spends

A minimal, well-structured expense tracking application built with Flask, React, and SQLite.

---

## Quick Start

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
flask shell                  # then run: from app.extensions import db; db.create_all(); exit()
flask run
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Backend runs on `http://127.0.0.1:5000` — Frontend on `http://localhost:5173`.

---

## Project Structure

```
clearspend/
├── backend/
│   ├── app/
│   │   ├── __init__.py          # App factory
│   │   ├── config.py            # Environment config
│   │   ├── extensions.py        # db and migrate instances
│   │   ├── models/
│   │   │   ├── category.py      # Category model
│   │   │   └── transaction.py   # Transaction model
│   │   ├── routes/
│   │   │   ├── categories.py    # Category endpoints
│   │   │   ├── transactions.py  # Transaction endpoints
│   │   │   └── summary.py       # Summary/aggregation endpoint
│   │   └── schemas/
│   │       ├── category_schema.py     # Category validation
│   │       └── transaction_schema.py  # Transaction validation
│   ├── tests/
│   │   ├── conftest.py              # Isolated in-memory test DB
│   │   ├── test_categories.py
│   │   ├── test_transactions.py
│   │   └── test_summary.py
│   ├── run.py
│   ├── pytest.ini
│   └── requirements.txt
└── frontend/
    └── src/
        ├── api/
        │   └── client.js            # Axios base config
        ├── components/
        │   ├── CategoryManager.jsx
        │   ├── TransactionManager.jsx
        │   └── Summary.jsx
        └── App.jsx
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/categories/` | List all active categories |
| POST | `/api/categories/` | Create a category |
| DELETE | `/api/categories/:id` | Soft-delete a category |
| GET | `/api/transactions/` | List transactions (filterable by category, date range) |
| POST | `/api/transactions/` | Create a transaction |
| DELETE | `/api/transactions/:id` | Soft-delete a transaction |
| GET | `/api/summary/` | Total spend per category and overall |

---

## Key Technical Decisions

### 1. Application Factory Pattern (`create_app`)

The Flask app is created inside a factory function rather than at module level. This allows the app to be instantiated with different configurations — production config for the real server, in-memory SQLite config for tests — without any code changes. It also eliminates circular import issues between routes, models, and extensions.

### 2. Extensions Isolated in `extensions.py`

`db` and `migrate` are created in their own file and initialized against the app inside `create_app()`. This is a deliberate separation: models import from `extensions`, routes import from `extensions`, and neither imports from `app/__init__.py`. This keeps the dependency graph acyclic and makes each module independently testable.

### 3. Soft Deletes on Both Models

Both `Category` and `Transaction` use an `is_deleted` flag rather than hard database deletes. The reasons are:

- **Referential integrity** — hard-deleting a category that has associated transactions would orphan those records. Soft delete keeps the history intact.
- **Auditability** — deleted data is preserved and diagnosable if something goes wrong.
- **Business rule enforcement** — before soft-deleting a category, the API checks whether any active (non-deleted) transactions reference it. If they do, the delete is blocked with a `409` error. This prevents the application from reaching an invalid state.

### 4. Validation at the Schema Layer (Marshmallow)

All incoming data is validated by Marshmallow schemas before it touches the database. This means:

- Amounts must be greater than zero — enforced in `TransactionSchema`
- Names cannot be blank or whitespace — enforced in `CategorySchema`
- Required fields are declared explicitly — missing fields return structured `400` errors

The database never receives invalid data. Business rules live in the route layer on top of schema validation (e.g., checking that a category exists before creating a transaction against it).

### 5. RESTful URL Design

URLs describe resources, not actions. The HTTP method carries the action meaning:

```
POST   /api/categories/    → create
GET    /api/categories/    → list
DELETE /api/categories/1   → delete
```

This keeps the API surface predictable — a new developer can understand every endpoint without reading its implementation.

### 6. Test Isolation with In-Memory SQLite

Each test runs against a fresh, isolated SQLite database created in memory and torn down after the test. This ensures tests cannot affect each other, running order does not matter, and the real `clearspend.db` is never touched during test runs.

---

## Running Tests

```bash
cd backend
pytest tests/ -v
```

All 18 tests should pass. Tests cover:

- Happy path creation for categories and transactions
- Duplicate category name rejection
- Blank/whitespace name rejection
- Negative and zero amount rejection
- Transaction creation against nonexistent or deleted category
- Category delete blocked when active transactions exist
- Filter by category on transaction list
- Summary total correctness
- Summary excluding soft-deleted transactions
- Empty summary state

---

## Tradeoffs and Weaknesses

**SQLite over PostgreSQL** — SQLite is sufficient for this scope and removes infrastructure setup entirely. In production, this would be swapped for PostgreSQL via a single `DATABASE_URL` environment variable change. SQLite does not support concurrent writes, which would be a hard limit in a real multi-user deployment.

**No authentication** — the API has no auth layer. Every endpoint is open. Adding JWT-based auth would be the first production requirement, implemented as a Flask middleware/decorator wrapping protected routes.

**Float for amounts** — monetary values are stored as `Float`. This is acceptable for demonstration purposes but a production system would use `Numeric(10, 2)` (fixed precision decimal) to avoid floating point rounding errors in financial calculations.

**No pagination** — the transactions list endpoint returns all records. For large datasets this would need `limit`/`offset` query params and a total count header.

**Frontend error granularity** — the frontend surfaces the first error message from the API response. In a production UI, field-level inline errors would be shown next to the relevant input rather than a single message below the form.

---

## Future Improvements

If this system needed to grow, the next steps in order of priority would be:

1. **Auth** — JWT tokens, user ownership of categories and transactions
2. **Pagination** — `limit`/`offset` on the transactions endpoint
3. **Edit support** — `PATCH /api/transactions/:id` and `PATCH /api/categories/:id`
4. **Date range filtering on summary** — month/year breakdown of spend
5. **PostgreSQL** — swap `DATABASE_URL` in `.env`, no code changes needed
6. **Dockerize** — single `docker-compose.yml` to run backend + frontend together