from datetime import datetime

from fastapi import HTTPException

import models
from schemas.answer import AnswerForUser
from schemas.question import QuestionForUser
from schemas.result import ResultCreate, ResponseResultCreate, Result


def get_all_results(db):
    return db.query(models.Result).all()


def get_result_by_user(id, db):
    return db.query(models.Result).filter_by(user_id=id).all()


def get_result_by_test(id, db):
    return db.query(models.Result).filter_by(test_id=id).all()


def get_result(id, db):
    return db.query(models.Result).filter_by(id=id).first()


# request: {'attemp_id':'','answers': [{'question_id':'','answer': {'$id_answer':ischoose}}, 'time_completion':]}
# def add_result(request, username, db):
#     attemp = db.query(models.Attemp).filter_by(user_id=username, id=request.attemp_id).first()
#     if attemp is None:
#         raise HTTPException(status_code=400, detail="Attemp not found")
#     score = 0
#     answers = attemp.answer_of_users
#     for answer in answers:
#         if answer.is_correct:
#             score += 1
#     new_result = models.Result(
#         user_id=username,
#         test_id=attemp.test_id,
#         completion_time=request.completion_time,
#         score=score
#     )
#     db.add(new_result)
#     db.commit()
#     db.refresh(new_result)
#     return new_result


def create_result(request: ResultCreate, username: str, db):
    user = db.query(models.User).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    test_user = db.query(models.TestUser).filter_by(user_id=user.id, test_id=request.test_id).first()
    if test_user is None:
        raise HTTPException(status_code=400, detail="You don't have permission to do this test")

    new_result = db.query(models.Result).filter_by(user_id=user.id, test_id=request.test_id).first()
    if new_result is not None:
        if new_result.test.limit == 1:
            if new_result.score is not None:
                raise HTTPException(status_code=400, detail="You have done this test")
            else:
                return new_result

    new_result = models.Result(test_id=request.test_id, user_id=user.id, start_time=datetime.now())
    db.add(new_result)
    db.commit()
    db.refresh(new_result)

    return new_result


def get_result_by_test_id_user(id_test: int, username: str, db, role: int = 2):
    user = db.query(models.User).filter_by(username=username).first()
    if user is None:
        raise HTTPException(status_code=400, detail="User not found")

    test_user = db.query(models.TestUser).filter_by(user_id=user.id, test_id=id_test).first()
    if test_user is None:
        raise HTTPException(status_code=400, detail="You don't have permission to do this test")

    result = db.query(models.Result).filter_by(user_id=user.id, test_id=id_test).first()
    if result is None:
        raise HTTPException(status_code=400, detail="You haven't done this test")

    if role == 1:
        return result
    if result.test.permission_review == 0:
        for i in range(len(result.answer_of_users)):
            result.answer_of_users[i].question.answers = []
    return result


def get_results_by_test_id(test_id, db):
    testuser_db = db.query(models.TestUser).filter_by(test_id=test_id).all()
    if testuser_db is None:
        raise HTTPException(status_code=400, detail="Test not found")

    results = []

    for testuser in testuser_db:
        result = db.query(models.Result).filter_by(user_id=testuser.user_id, test_id=test_id).first()
        if result is None:

            results.append(Result(user=testuser.user))
        else:
            results.append(Result(user=testuser.user, id=result.id, completion_time=result.completion_time, score=result.score))

    return results

