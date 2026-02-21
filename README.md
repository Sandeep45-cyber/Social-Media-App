# Social Media API (FastAPI + PostgreSQL)

A production-style CRUD API for social posts built with FastAPI, SQLAlchemy, and PostgreSQL.

## Demo

- API docs (Swagger): `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Features

- Create, read, update, and delete posts
- SQLAlchemy ORM with relational persistence
- Request/response schema validation with Pydantic
- Containerized API + Postgres stack with Docker Compose
- CI pipeline for linting and tests

## Tech Stack

- Python 3.12
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pytest + HTTPX
- Ruff
- Docker + Docker Compose
- GitHub Actions

## Project Structure

```text
.
├── app/
│   ├── database.py
│   ├── main.py
│   ├── models.py
│   └── schemas.py
├── tests/
│   └── test_posts.py
├── .github/workflows/ci.yml
├── docker-compose.yml
├── Dockerfile
└── requirements.txt
```

## How To Run Locally

### Option 1: Python environment

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
```

### Option 2: Docker Compose

```bash
docker compose up --build
```

This starts:
- API at `http://localhost:8000`
- Swagger at `http://localhost:8000/docs`
- PostgreSQL on port `5432`

## Environment Variables

- `DATABASE_URL` (required)
  - Example: `postgresql+psycopg://postgres:postgres@localhost:5432/fastapi`

## API Endpoints

- `GET /` health message
- `GET /posts` list posts
- `POST /posts` create post
- `GET /posts/{id}` fetch a single post
- `PUT /posts/{id}` update post
- `DELETE /posts/{id}` delete post

## Architecture / Design

```text
Client -> FastAPI (app/main.py) -> SQLAlchemy Session -> PostgreSQL
                    |                       |
                    |                       -> ORM model mapping (app/models.py)
                    -> Pydantic schema validation (app/schemas.py)
```

## Key Engineering Choices

- Dependency-injected DB session (`get_db`) keeps handlers testable and consistent.
- `DATABASE_URL` based configuration supports local, Docker, and CI environments.
- ORM + response schemas enforce type safety and predictable API contracts.
- Separate tests use SQLite to validate API behavior quickly in CI.

## Testing

```bash
pytest -q
```

## Linting

```bash
ruff check .
```

## CI

GitHub Actions workflow runs lint + tests on push and pull requests.

![CI](https://github.com/Sandeep45-cyber/python/actions/workflows/ci.yml/badge.svg)
