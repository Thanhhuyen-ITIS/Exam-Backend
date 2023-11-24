from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from config import database
from repository import test_repo
from schemas.test import Test, TestCreate, ResponseTestInforForUser
from schemas.user import TokenData
from services.oauth2 import get_current_admin, get_current_user

router = APIRouter(tags=['Test'])

get_db = database.get_db


@router.get('/tests', response_model=Page[Test])
def get_tests(db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return paginate(test_repo.get_tests(db))

@router.get('/topic/{id}/tests', response_model=list[ResponseTestInforForUser])
def get_tests_by_topic(id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return test_repo.get_tests_by_topic(id=id, db=db)


# for user
@router.get('/user/topic/{id}/tests', response_model=list[Test])
def get_tests_by_topic(id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_user)):
    return test_repo.get_tests_by_topic(id, tokendata.username, db)


@router.get('/test/{id}', response_model=TestCreate)
def get_test(id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_user)):
    return test_repo.get_test(id, db)


@router.post('/create_test')
def add_test(request: TestCreate, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    test_repo.add_test(request, db)


@router.delete('/delete_test/{id}')
def delete_test(id: int, db: Session = Depends(get_db), tokenData: TokenData = Depends(get_current_admin)):
    return test_repo.delete_test(id, db)


# update test
@router.put('/update_test/{id}')
def update_test(id: int, request: TestCreate, db: Session = Depends(get_db),
                tokendata: TokenData = Depends(get_current_admin)):
    return test_repo.update_test(id, request, db)
