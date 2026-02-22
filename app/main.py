"""FastAPI application and HTTP handlers for posts."""

from typing import List

from fastapi import Depends, FastAPI, HTTPException, Response, status
from sqlalchemy.orm import Session

from . import models, schemas
from .database import Base, engine, get_db

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Social Media API",
    description="Simple FastAPI CRUD service for posts",
    version="1.0.0",
)


@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    """Return all posts directly from SQLAlchemy as a quick DB check."""
    posts = db.query(models.Post).all()
    return {"status": posts}


@app.get("/")
async def root():
    """Return a simple service health message."""
    return {"message": "Hello World"}


@app.get("/posts", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    """List all posts."""
    posts = db.query(models.Post).all()
    return posts


@app.post("/posts", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def cpost(post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Create and persist a new post."""
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/{id}")
def get_post(id: int, db: Session = Depends(get_db)):
    """Fetch one post by its identifier."""
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"The post with id {id} was not found")

    return {"data": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    """Delete a post if it exists."""
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() is None:
        raise HTTPException(status_code=404, detail=f"Id {id} not found")

    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    """Update title/content/published fields for an existing post."""
    updatedpost = db.query(models.Post).filter(models.Post.id == id)

    if updatedpost.first() is None:
        raise HTTPException(status_code=404, detail=f"Id {id} not found")

    updatedpost.update(
        {
            models.Post.title: post.title,
            models.Post.content: post.content,
            models.Post.published: post.published,
        },
        synchronize_session=False,
    )

    db.commit()

    return {"data": updatedpost.first()}
