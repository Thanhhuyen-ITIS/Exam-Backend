import json

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

import models
from config.database import get_db
from repository import result_repo
from schemas.answer import Answer, AnswerForUser
from schemas.answer_of_user import RequestAnswersOfUser


def get_all_answer_of_user(attemp_id: int, db: Session = Depends(get_db)):
    return db.query(models.AnswerOfUser).filter(models.AnswerOfUser.attemp_id == attemp_id).all()


# request: {'attemp_id':'','answers': [{'question_id':'','answer': {'$id_answer':ischoose}}, 'time_complete':]}
#{"attemp_id": ,"answers": [{"question_id": ,"answer": {"$id_answer":ischoose}}, "time_complete":] change it to json
# request: {'attemp_id':1,
#           'answers': [
#              {'question_id':'1',
#               'answer': {'1':False, '2':True, '3':False, '4':False}},
#              {'question_id':'2',
#               'answer': {'5':False, '6':False, '6':True, '8':False}}
#            ]
#         }


def check_answer(options: list[Answer], answers: list[AnswerForUser]):
    options.sort(key=lambda x: x.id)
    answers.sort(key=lambda x: x.id)

    for i in range(len(options)):
        if options[i].is_correct_answer != answers[i].is_selected:
            return False
    return True

def create_answers_of_user(request: RequestAnswersOfUser, username: str, db):
    try:
        user = db.query(models.User).filter(models.User.username == username).first()
        result_db = db.query(models.Result).filter(models.Result.user_id == user.id,
                                                    models.Result.id == request.result_id).first()
        score = 0
        if result_db is None:
            raise HTTPException(status_code=400, detail="Result not found")

        for answer in request.answers:
            question = db.query(models.Question).filter(models.Question.id == answer.question_id).first()
            if question is None:
                raise HTTPException(status_code=400, detail="Question not found")

            question_test = db.query(models.QuestionTest).filter(models.QuestionTest.question_id == answer.question_id, models.QuestionTest.test_id == result_db.test_id).first()
            if question_test is None:
                raise HTTPException(status_code=400, detail="Question not in this test")

            answer_of_user_db = db.query(models.AnswerOfUser).filter(models.AnswerOfUser.result_id == request.result_id,
                                                             models.AnswerOfUser.question_id == answer.question_id).first()
            if answer_of_user_db is not None:
                raise HTTPException(status_code=400, detail="Answer of question already exist")

            new_answer_of_user = models.AnswerOfUser(
                result_id=request.result_id,
                question_id=answer.question_id,
                answer=[x.dict() for x in answer.answer],
                is_correct=check_answer(question.answers, answer.answer),
            )
            score += new_answer_of_user.is_correct
            db.add(new_answer_of_user)

        result_db.end_time = request.end_time
        result_db.completion_time = (request.end_time - result_db.start_time).total_seconds()
        result_db.score = score/request.answers.__len__() * 10
        db.commit()
    except Exception as e:
        db.rollback()
        print(e)
        raise HTTPException(status_code=400, detail="Something went wrong")

    return result_db



