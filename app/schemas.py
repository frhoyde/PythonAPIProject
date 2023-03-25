#!/usr/bin/env python3
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):
    title: str
    content: str
    published: bool = False

class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: EmailStr

class UserCredentials(UserBase):
    password: str


class User(UserBase):
    id: int
    created_at: datetime
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str]
