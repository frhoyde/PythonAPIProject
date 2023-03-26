#!/usr/bin/env python3
from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCredentials(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    creator_id: int
    creator: User
    class Config:
        orm_mode = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]

class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)
