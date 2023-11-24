from datetime import datetime

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models
from config.database import get_db


def get_topics(db: Session = Depends(get_db)):
    return db.query(models.Topic).all()


# def get_topics_for_user(db: Session = Depends(get_db), username: str = None):
#     user_id = db.query(models.User).filter_by(username=username).first().id
#     tests_user = db.query(models.TestUser).filter_by(user_id=user_id).all()
#     tests = [test.test for test in tests_user]
#     test_topic = [test.test_topics for test in tests]
#     topics = [topic.topic for topic in test_topic]
#
#     return topics

# optimize function get_topics_for_user
def get_topics_for_user(db: Session = Depends(get_db), username: str = None):
    user_id = db.query(models.User).filter_by(username=username).first().id
    topics = db.query(models.Topic).join(models.TestTopic).join(models.Test).join(models.TestUser).filter(models.TestUser.user_id == user_id).all()
    return topics

def get_topic(id: int, db: Session = Depends(get_db)):
    return db.get(models.Topic, id)


def add_topic(request, db: Session = Depends(get_db)):
    new_topic = db.query(models.Topic).filter_by(topic_name=request.topic_name).first()

    if not new_topic:
        new_topic = models.Topic(topic_name=request.topic_name, topic_image=request.topic_image, create_time=datetime.now())
        db.add(new_topic)
        db.commit()
    else:
        raise HTTPException(status_code=400, detail=f'Tạo Topic không thành công')

    return {
        'status': 200,
        'message': 'Tạo Topic thành công'
    }


def update_topic(id: int, request, db: Session = Depends(get_db)):
    topic = db.query(models.Topic).filter_by(id=id).first()

    if not topic:
        raise HTTPException(status_code=400, detail=f'Không tìm thấy Topic có id = {id}')

    topic.topic_name = request.topic_name
    topic.topic_image = request.topic_image

    db.commit()
    db.refresh(topic)
