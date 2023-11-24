from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from config.database import get_db
from repository import question_repo
from schemas.question import Question
from schemas.user import TokenData
from services.oauth2 import get_current_admin

router = APIRouter(tags=['Question'])

@router.get('/questions', response_model=Page[Question])
def get_questions(db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return paginate(question_repo.get_questions(db))

@router.post('/create_question')
def add_question(request: Question, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    question_repo.add_question(request, db)

#api delete question
@router.delete('/delete_question/{id}')
def delete_question(id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    question_repo.delete_question(id, db)

#api update question
@router.put('/update_question/{id}')
def update_question(id: int, request: Question, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return question_repo.update_question(id, request, db)