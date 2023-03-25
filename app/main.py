#!/usr/bin/env python3
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas
from .database import engine, get_db

# To create akk the models
models.Base.metadata.create_all(bind=engine)



# Instance of FastAPI
app = FastAPI()
############################
# uvicorn main:app --reload
############################



while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='pythonapiproject', user='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Connected!')
        break
    except Exception as error:
        print(error)


@app.get("/")
async def root():
    return my_post


@app.get("/posts")
def get_posts(db: Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    posts = db.query(models.Post).all()
    # print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):

    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return {"message": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response, db: Session = Depends(get_db)):

    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    post.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):

    find_post_query = db.query(models.Post).filter(models.Post.id == id)

    if find_post_query.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")


    find_post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return {"Update Post": find_post_query.first()}
