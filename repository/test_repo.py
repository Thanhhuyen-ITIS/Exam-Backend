from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models
from config.database import get_db
from repository import topic_detail_repo
from schemas.test import Test, TestCreate
from schemas.topic_detail import TopicDetail


def get_tests(db: Session = Depends(get_db)):
    return db.query(models.Test).all()


def get_test(id: int, db: Session = Depends(get_db)):
    test_db = db.query(models.Test).filter(models.Test.id == id).first()
    if not test_db:
        raise HTTPException(status_code=404, detail='Test not found')

    test = TestCreate(id=test_db.id, test_name=test_db.test_name, start_time=test_db.start_time,
                      end_time=test_db.end_time, duration=test_db.duration, topic_id=test_db.test_topics[0].topic_id,
                      limit=test_db.limit, permission_review=test_db.permission_review)
    return test


def get_tests_by_topic(id: int, username: str = None, db: Session = Depends(get_db)) -> object:
    if username is None:
        return db.query(models.Test).join(models.TestTopic).filter(models.TestTopic.topic_id == id).all()

    user_id = db.query(models.User).filter(models.User.username == username).first().id

    result_db = db.query(models.Test).join(models.TestUser).join(models.TestTopic).filter(
        models.TestTopic.topic_id == id, models.TestUser.user_id == user_id).all()
    return result_db


def add_test(request, db: Session):
    new_test = db.query(models.Test).filter(models.Test.test_name == request.test_name).first()
    if new_test:
        topic = new_test.topic
        if topic.topic_id == request.topic_id:
            raise HTTPException(status_code=400, detail='Test da ton tai')
    else:
        new_test = models.Test(test_name=request.test_name, start_time=request.start_time, end_time=request.end_time,
                               duration=request.duration, permission_review=request.permission_review)
        db.add(new_test)
        db.commit()
        db.refresh(new_test)
        topic_detail_repo.add_topic_detail(TopicDetail(topic_id=request.topic_id, test_id=new_test.id), db)
    return {
        'status': 200,
        'message': 'Test created successfully'
    }


def delete_test(id: int, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == id).first()
    if not test:
        raise HTTPException(status_code=404, detail='Test not found')
    else:
        db.delete(test)
        db.commit()
        return 'Delete success'


def update_test(id: int, request: TestCreate, db: Session = Depends(get_db)):
    test = db.query(models.Test).filter(models.Test.id == id).first()
    if not test:
        raise HTTPException(status_code=404, detail='Test not found')
    else:
        test.test_name = request.test_name
        test.start_time = request.start_time
        test.end_time = request.end_time
        test.duration = request.duration
        test.limit = request.limit
        test.permission_review = request.permission_review
        db.commit()
        db.refresh(test)
        return test
