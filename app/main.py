#!/usr/bin/env python3
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import post, user, auth, vote
from .config import settings

# To create all the models
models.Base.metadata.create_all(bind=engine)

# Instance of FastAPI
app = FastAPI()

############################
# uvicorn main:app --reload
############################

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")
async def root():
    return {"App":"Run"}
