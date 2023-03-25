#!/usr/bin/env python3
from fastapi import APIRouter, status, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from .. import schemas, models, utils
from ..database import get_db

router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)

@router.post('/login')
def login(user_credentials: schemas.UserCredentials ,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.email).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Invalid Credentials")

    return { "token": "Example"}




def logout():
    pass
