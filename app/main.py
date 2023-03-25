#!/usr/bin/env python3
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
# Instance of FastAPI
app = FastAPI()
############################
# uvicorn main:app --reload
############################

class Post(BaseModel):
    title: str
    content: str
    published: bool = False

while True:
    try:
        conn = psycopg2.connect(host='localhost', dbname='pythonapiproject', user='postgres', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print('Database Connected!')
        break
    except Exception as error:
        print(error)


my_post = [{"title": "title 1", "content": "content 1", "id":1}, {"title": "title 2", "content": "content 2", "id": 2}]

def find_post(id):
    for i in my_post:
        if i["id"] == id:
            return i


@app.get("/")
async def root():
    return my_post

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s,%s,%s) RETURNING *""", (post.title, post.content, post.published))
    new_post = cursor.fetchone();
    conn.commit()
    return {"message": new_post}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    post = cursor.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    conn.commit()
    # print(post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""", (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")

    conn.commit()
    return {"Update Post": updated_post}
