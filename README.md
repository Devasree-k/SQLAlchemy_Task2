# Simple Transport Collection API

This version keeps the project focused on the SQLAlchemy relationship and JOIN concept.

## Setup

1. Create a PostgreSQL database named `transport_db`.
2. Copy `.env.example` to `.env` and enter your PostgreSQL password.
3. Install packages: `pip install -r requirements.txt`
4. Run: `uvicorn main:app --reload`
5. Open `http://127.0.0.1:8000/docs`

Tables are created by `Base.metadata.create_all()` in `main.py` when the app starts. This is convenient for a learning project; use Alembic migrations for production schema changes.

## Main endpoints

- `POST /api/drivers/` — create a driver
- `GET /api/drivers/` — list drivers
- `GET /api/drivers/{driver_id}` — get one driver
- `POST /api/collections/` — create a collection
- `GET /api/collections/` — list collections with driver details
- `GET /api/collections/{collection_id}` — get one collection with driver details
- `PATCH /api/collections/{collection_id}` — update supplied fields
- `DELETE /api/collections/{collection_id}` — delete a collection

Collection totals are calculated by the service, not accepted from the client.
