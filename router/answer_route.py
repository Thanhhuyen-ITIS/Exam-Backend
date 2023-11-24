from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import answer_repo
from schemas.answer import Answer

router = APIRouter(tags=['Answer'])


@router.post('/answer')
def add_answer(request: Answer, db: Session = Depends(get_db)):
    return answer_repo.add_answer(request, db)

# delete answer
@router.delete('/answer/{id}')
def delete_answer(id: int, db: Session = Depends(get_db)):
    return answer_repo.delete_answer(id, db)
