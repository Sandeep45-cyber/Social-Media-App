"""API tests for post CRUD endpoints using a SQLite test database."""

import os

os.environ["DATABASE_URL"] = "sqlite:///./test.db"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Provide a test-scoped database session to FastAPI dependencies."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    """Reset DB schema between tests for isolated behavior."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_post():
    """Creating a post should return 201 and echoed content."""
    res = client.post(
        "/posts",
        json={"title": "Hello", "content": "World", "published": True},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Hello"
    assert body["content"] == "World"


def test_get_posts():
    """Listing posts should include previously created records."""
    client.post(
        "/posts",
        json={"title": "A", "content": "B", "published": True},
    )

    res = client.get("/posts")
    assert res.status_code == 200
    body = res.json()
    assert len(body) == 1
    assert body[0]["title"] == "A"


def test_delete_missing_post():
    """Deleting an unknown post id should return 404."""
    res = client.delete("/posts/999")
    assert res.status_code == 404
