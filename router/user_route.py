from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from config import database
from repository import user_repo
from schemas.user import UserCreate, User, TokenData
from services.oauth2 import get_current_admin, get_current_user

router = APIRouter(tags=['User'])

get_db = database.get_db


@router.post('/create_user')
def add_user(request: UserCreate, db: Session = Depends(get_db)):
    return user_repo.create(request, db)

@router.get('/me', response_model=TokenData)
def get_me(tokendata: TokenData = Depends(get_current_user)):
    return tokendata


@router.get('/user', response_model=User)
def get_user(tokendata: TokenData = Depends(get_current_user), db: Session = Depends(get_db)):
    return user_repo.get_user(tokendata.username, db)


@router.get('/user/{username}', response_model=User)
def get_user(username: str, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return user_repo.get_user(username, db)


@router.get('/users', response_model=Page[User])
def get_users(db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return paginate(user_repo.get_users(db))
