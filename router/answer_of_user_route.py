from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import answer_of_user_repo
from schemas.answer_of_user import RequestAnswersOfUser
from schemas.result import ResponseResultDetail
from services.oauth2 import get_current_user

router = APIRouter(tags=['AnswerOfUser'])

@router.post('/create_answers_of_user')
def create_answers_of_user(request: RequestAnswersOfUser, db: Session = Depends(get_db),
                           tokendata=Depends(get_current_user)):
    return answer_of_user_repo.create_answers_of_user(request, tokendata.username, db)

