from random import randrange
from typing import Optional
from fastapi import Body, FastAPI, HTTPException, Response, status, Depends
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models, schemas
from .database import engine, Base, get_db
from sqlalchemy.orm import Session



Base.metadata.create_all(bind=engine)





try:
    conn = psycopg2.connect(host = 'localhost', database='fastApi', user='postgres',
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database connection was successful")
except Exception as error:
    print("Connecting to database failed")
    print(error)



app = FastAPI()

@app.get("/sqlalchemy")
def test_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return {"status" : posts}


@app.get("/")
async def root():
    return {"message" : "Hello World"} 

@app.get("/posts")
def get_posts(db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    print(posts)
    return {"data" : posts}


@app.post("/posts", status_code= status.HTTP_201_CREATED, response_model=schemas.Post)
def cpost(post: schemas.PostCreate, db: Session=Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.content, post.published))
    # new_post = cursor.fetchone()

    # conn.commit()
    new_post = models.Post(**post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)


    return new_post





@app.get("/posts/{id}")
def get_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s """, (str(id),))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=404, detail=f"The post with id {id} was not found")


    return {"data":post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session=Depends(get_db)):
    # cursor.execute(""" DELETE from posts where id = %s RETURNING * """, (str(id), ),)
    # del_post = cursor.fetchone()

    # conn.commit()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.filter() == None:
        raise HTTPException(status_code=404, detail=f"Id {id} not found")
    
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
async def update_post(id:int, post: schemas.PostCreate, db: Session=Depends(get_db)):
    # cursor.execute(""" update posts set title = %s,  content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)) )
    # updatedpost = cursor.fetchone()
    # conn.commit()

    updatedpost = db.query(models.Post).filter(models.Post.id == id)

    if updatedpost.first() is None:
        raise HTTPException(status_code=404, detail=f"Id {id} not found")

    updatedpost.update(**post.model_dump(), synchronize_session=False)

    db.commit()

    return {"data" : updatedpost.first()}
