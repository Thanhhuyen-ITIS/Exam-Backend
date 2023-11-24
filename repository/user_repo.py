from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models
from config.database import get_db
from schemas.user import UserCreate
from security.hashing import Hash


def create(request: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == request.username).first()
    if db_user:
        raise HTTPException(status_code=500, detail=f' Tài khoản {request.username} đã tồn tại')
    new_user = models.User(username=request.username, password=Hash.bcrypt(request.password))

    db.add(new_user)
    db.commit()


    return {'status': 200,
        'message': 'User created successfully'}


def get_users(db: Session = Depends(get_db())):
    return db.query(models.User).all()

def get_user_detail(username: str, db: Session = Depends(get_db())):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f'User not found')

def get_user(username: str, db: Session = Depends(get_db())):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if not db_user:
        raise HTTPException(status_code=404, detail=f'User not found')
    return db_user