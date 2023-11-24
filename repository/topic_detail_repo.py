from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
from schemas.test import Test


def add_topic_detail(request, db: Session):
    new_topic_detail = db.query(models.TestTopic).filter_by(topic_id=request.topic_id,
                                                              test_id=request.test_id).first()

    if new_topic_detail is None:
        new_topic_detail = models.TestTopic(topic_id=request.topic_id, test_id=request.test_id)
        db.add(new_topic_detail)
        db.commit()
    else:
        raise HTTPException(status_code=400, detail="Topic detail already exists")


def delete_topic_detail(id: int, db: Session):
    topic_detail = db.query(models.TestTopic).filter_by(id=id).first()

    if topic_detail is None:
        raise HTTPException(status_code=404, detail="Topic detail not found")
    else:
        db.delete(topic_detail)
        db.commit()


def get_about_topic(topic_id: int, db: Session):
    topic_detail = db.query(models.TestTopic).filter_by(topic_id=topic_id).all()
    data = []
    for i in topic_detail:
        # change test in model to test schema
        test = Test(id=i.test.id, test_name=i.test.test_name, start_time=i.test.start_time, end_time=i.test.end_time, duration=i.test.duration, limit=i.test.limit)
        data.append(test)
    return data


