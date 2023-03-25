#!/usr/bin/env python3
from typing import List
from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import engine, get_db
from .routers import post, user, auth

# To create all the models
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



app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)


@app.get("/")
async def root():
    return {"App":"Run"}
