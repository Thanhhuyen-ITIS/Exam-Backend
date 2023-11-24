from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.database import get_db
from repository import topic_repo
from schemas.topic import TopicBase, Topic
from schemas.user import TokenData
from services.oauth2 import get_current_admin, get_current_user

router = APIRouter(tags=['Topic'])

@router.get('/topics')
def get_topics(db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_user)):
    if tokendata.role == 1:
        return topic_repo.get_topics(db)
    return topic_repo.get_topics_for_user(db, tokendata.username)

@router.post('/create_topic')
def add_topic(request: Topic, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    topic_repo.add_topic(request, db)

@router.get('/topic/{id}', response_model=Topic)
def get_topic(id: int, db: Session = Depends(get_db)):
    if id == -1:
        return Topic()
    return topic_repo.get_topic(id, db)

#update topic
@router.put('/topic/{id}')
def update_topic(id: int, request: TopicBase, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):

    return topic_repo.update_topic(id, request, db)