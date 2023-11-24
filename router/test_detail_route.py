from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from config.database import get_db
from repository import test_detail_repo
from schemas.question import Question

from schemas.user import TokenData
from services.oauth2 import get_current_admin

router = APIRouter(tags=['QuestionTest'])


# create api get_test_detail with parameter test_id in here
@router.get('/get_test_detail/{test_id}', response_model=list[Question])
def get_test_detail(test_id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return test_detail_repo.get_test_detail(test_id, db)


@router.post('/create_test_detail/{test_id}')
def add_test_detail(test_id: int, request: list, db: Session = Depends(get_db)):

    return test_detail_repo.add_test_detail(test_id, request, db)


@router.delete('/delete_test_detail/{test_id}/{question_id}')
def delete_test_detail(test_id, question_id, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    test_detail_repo.delete_test_detail(test_id, question_id, db)


# get about test
@router.get('/about_test/{test_id}')
def get_about_test(test_id: int, db: Session = Depends(get_db)):
    return test_detail_repo.get_about_test(test_id, db)
