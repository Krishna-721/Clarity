# AI Guidance for Clarity

This file defines the rules, constraints, and standards that governed AI assistance during the development of Clarity — Know your spends. Any AI agent working on this codebase must follow these instructions.

---

## Project Context

Clarity is a minimal expense tracker. The goal is a small, correct, well-structured system — not a feature-rich one. Every decision should prioritize clarity and correctness over cleverness or completeness.

---

## Non-Negotiable Constraints

### 1. Never bypass the schema validation layer
All incoming request data must pass through Marshmallow schemas before reaching route logic or the database. Do not add database writes or reads that skip schema validation, even for "internal" operations.

### 2. Never hard-delete Category or Transaction records
Both models use soft deletes (`is_deleted = True`). Never generate code that calls `db.session.delete()` on a Category or Transaction. Always set `is_deleted = True` and commit.

### 3. Never allow a Category to be deleted if it has active transactions
Before soft-deleting a Category, always call `category.has_transactions()`. If it returns `True`, return a `409` error. This business rule must never be removed or weakened.

### 4. Never store a Transaction against a deleted or nonexistent Category
Before inserting a Transaction, always verify the referenced Category exists and has `is_deleted = False`. If not, return a `404` error.

### 5. Never allow amounts of zero or below
`TransactionSchema.validate_amount` enforces `amount > 0`. Do not change this threshold or remove this validator.

### 6. Never allow blank or whitespace-only category names
`CategorySchema.validate_name` enforces `value.strip()` is non-empty. Do not remove or weaken this check.

---

## Architecture Rules

### App factory pattern is required
The Flask app must always be created inside `create_app()`. Do not instantiate the app at module level. Do not import `app` directly from `__init__.py` in routes or models.

### `db` and `migrate` must stay in `extensions.py`
Never move `db = SQLAlchemy()` into `__init__.py` or any model file. All models and routes import `db` from `app.extensions`. This prevents circular imports.

### Blueprints only — no global route decorators
All routes must be registered on a Blueprint. Never use `@app.route(...)` directly.

### One Blueprint per resource
Categories, transactions, and summary each have their own Blueprint and route file. Do not merge them.

---

## Code Style Rules

- **Simple over clever** — if there are two ways to do something, use the more readable one
- **Explicit over implicit** — name variables clearly, avoid single-letter names outside loop counters
- **No unused imports** — remove any import that is not referenced in the file
- **No commented-out code** — delete dead code, don't comment it out
- **Error messages must be user-readable** — never return raw SQLAlchemy exceptions or Python tracebacks to the client
- **All responses must be JSON** — never return plain text or HTML from API routes

---

## What AI Is Allowed To Do

- Add new fields to existing models (with a corresponding migration)
- Add new endpoints following the existing Blueprint and schema pattern
- Add new test cases to existing test files
- Refactor internals of a function as long as its behavior and return contract stay the same
- Suggest improvements with a clear explanation of the tradeoff

---

## What AI Must Not Do

- Remove or weaken any existing validation rule
- Change HTTP status codes for existing error responses
- Add direct SQL queries (`db.engine.execute`, raw `text()`) that bypass the ORM
- Introduce new global state or module-level side effects
- Add frontend logic that bypasses API validation (e.g., silently coercing negative amounts to positive before sending)
- Generate code that swallows exceptions silently with bare `except: pass`
- Add dependencies without updating `requirements.txt`

---

## Testing Rules

- Every new route or business rule must have at least one test for the happy path and one for the failure/edge case
- Tests must use the `client` fixture from `conftest.py` — never use the real `clarity.db`
- Tests must not depend on each other or share state
- Test function names must describe what they are asserting, e.g. `test_create_transaction_negative_amount` not `test_bad_input`

---

## How AI Assistance Was Used in This Project

AI was used as a pair programmer throughout this project. The following describes how AI output was handled:

- **All generated code was read and understood before being accepted** — no code was blindly copy-pasted
- **Business rules were defined by the developer, not the AI** — the soft-delete pattern, the category-transaction constraint, and the validation thresholds were specified as requirements before code was generated
- **AI suggestions were challenged when unclear** — for example, the reason for using the app factory pattern and isolating `db` in `extensions.py` was asked about and understood before adoption
- **Tests were used to verify AI-generated logic** — every route was tested against both valid and invalid inputs to confirm the generated code behaved as specified
- **This `claude.md` file was written to constrain future AI behavior** — so that any subsequent AI assistance operates within the same rules that governed the original build

---

## How This File Was Created

Clarity was built interactively with Claude (Anthropic) via a conversational interface. Prompts were not written upfront as structured files — instead, development happened step by step, with each decision discussed and understood before moving forward. This file captures the constraints and standards that emerged from that process, formalized so that any future AI assistance on this codebase operates within the same boundaries. The rules here are not generated boilerplate — they reflect the actual decisions made during the build and the reasoning behind them.