from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import result_repo
from schemas.result import ResultCreate, ResponseResultCreate, ResponseResultDetail, Result
from schemas.user import TokenData
from services.oauth2 import get_current_user, get_current_admin

router = APIRouter(tags=['Result'])


@router.get('/user/test/{test_id}/result', response_model=ResponseResultDetail)
def get_result_by_test_id_user(test_id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_user)):
    return result_repo.get_result_by_test_id_user(test_id, tokendata.username, db)


# add result
@router.post('/create_result', response_model=ResponseResultCreate)
def add_result(request: ResultCreate, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_user)):
    return result_repo.create_result(request, tokendata.username, db)


@router.get('/test/{test_id}/results', response_model=list[Result])
def get_results_by_test_id(test_id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_user)):
    return result_repo.get_results_by_test_id(test_id, db)

@router.get('/{username}/test/{test_id}/result', response_model=ResponseResultDetail)
def get_result_by_test_id_user(test_id: int, username: str, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return result_repo.get_result_by_test_id_user(test_id, username, db, tokendata.role)
