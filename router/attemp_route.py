from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import attemp_repo
from schemas.attemp import Attemp, AttempCreate
from services.oauth2 import get_current_user

router = APIRouter(tags=['Attemp'])

# get by test id
@router.get('/attemp_by_test/{id}')
def get_attemp_by_test(id: int, db: Session = Depends(get_db)):
    return attemp_repo.get_attemp_by_test(id, db)

#add attemp
@router.post('/attemp')
def add_attemp(request:AttempCreate, db: Session = Depends(get_db), tokendata = Depends(get_current_user)):
    return attemp_repo.add_attemp(request, tokendata.username, db)



