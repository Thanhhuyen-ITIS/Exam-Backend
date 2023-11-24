from fastapi import APIRouter, Depends
from fastapi_pagination import Page, paginate
from sqlalchemy.orm import Session

from config.database import get_db
from repository import topic_detail_repo
from schemas.test import Test
from schemas.topic_detail import TopicDetail
from schemas.user import TokenData
from services.oauth2 import get_current_admin

router = APIRouter(tags=['TestTopic'])

@router.post('/create_topic_detail')
def add_topic_detail(request: TopicDetail, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    topic_detail_repo.add_topic_detail(request, db)

@router.delete('/delete_topic_detail/{id}')
def delete_topic_detail(id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    topic_detail_repo.delete_topic_detail(id, db)


#get all test by topic_id
@router.get('/about_topic/{topic_id}', response_model=Page[Test])
def get_about_topic(topic_id: int, db: Session = Depends(get_db), tokendata: TokenData = Depends(get_current_admin)):
    return paginate(topic_detail_repo.get_about_topic(topic_id, db))

