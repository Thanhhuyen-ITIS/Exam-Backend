from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import test_user_repo
from schemas.test_user import TestUserCreate
from schemas.user import TokenData
from services.oauth2 import get_current_user, get_current_admin

router = APIRouter(tags=['TestUser'])

@router.get('/test_user')
def test_user():
    return {'message': 'Hello User'}


@router.post('/test_user')
def test_user(request: TestUserCreate, tokendata: TokenData = Depends(get_current_admin), db: Session = Depends(get_db)):

    test_user_repo.create_test_user(request, tokendata.username, db)
