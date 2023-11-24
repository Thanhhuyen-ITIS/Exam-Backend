from fastapi import HTTPException

import models
from schemas.test_user import TestUserCreate


def create_test_user(request: TestUserCreate, username: str, db):
    user = db.query(models.User).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    new_test_user = models.TestUser(test_id=request.test_id, user_id=user.id)
    db.add(new_test_user)
    db.commit()

    return {'message': 'Success'}
