from fastapi import HTTPException

import models


def get_attemp_by_test(id, db):
    return db.query(models.Attemp).filter_by(test_id=id).all()

def add_attemp(request, username, db):
    new_attemp = db.query(models.Attemp).filter_by(user_id=username, test_id=request.test_id).first()
    if new_attemp is not None:
        raise HTTPException(status_code=400, detail="Attemp already exists")
    new_attemp = models.Attemp(
        user_id=username,
        test_id=request.test_id,
    )
    db.add(new_attemp)
    db.commit()
    db.refresh(new_attemp)
    return new_attemp