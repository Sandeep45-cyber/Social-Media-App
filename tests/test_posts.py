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
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def test_create_post():
    res = client.post(
        "/posts",
        json={"title": "Hello", "content": "World", "published": True},
    )
    assert res.status_code == 201
    body = res.json()
    assert body["title"] == "Hello"
    assert body["content"] == "World"


def test_get_posts():
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
    res = client.delete("/posts/999")
    assert res.status_code == 404
