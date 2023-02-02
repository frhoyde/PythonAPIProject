#!/usr/bin/env python3
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
# Instance of FastAPI
app = FastAPI()
############################
# uvicorn main:app --reload
############################

class Post(BaseModel):
    title: str
    content: str
    rating: int = None #This means that it is optional

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
    return {"data": "Posts"}

@app.post("/post", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    post_dict = post.dict()
    post_dict['id'] = randrange(0, 100000000)
    my_post.append(post_dict)
    print(post.dict())
    return {"message": post_dict}

@app.get("/post/{id}")
def get_post(id: int, response: Response):
    post  = find_post(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not Found")
    return {"post_detail": post}


@app.delete("/post/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, response: Response):
    post_index = find_post_index(id)
    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    my_post.pop(post_index)
    print(my_post)
    return Response(status_code=status.HTTP_204_NO_CONTENT)

def find_post_index(id):
    for i, p in enumerate(my_post):
        if p["id"] == id:
            return i
    return None

@app.put("/post/{id}", status_code=status.HTTP_206_PARTIAL_CONTENT)
def update_post(id: int, post: Post):
    post_index = find_post_index(id)
    if not post_index:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post Not Found")
    post_dict = post.dict()
    post_dict["id"] = id
    my_post[post_index] = post_dict
    return {"Update Post": my_post[post_index]}
