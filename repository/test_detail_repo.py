from fastapi import HTTPException
from sqlalchemy.orm import Session
from starlette import status

import models
from schemas.question import Question


# create def get_test_detail with parameter test_id and db in here
def get_test_detail(test_id: int, db: Session):  # for admin
    test_details = db.query(models.QuestionTest).filter_by(test_id=test_id).all()
    questions = []
    for test_detail in test_details:
        questions.append(Question(id=test_detail.question.id, question_id=test_detail.question.question_id,
                                  question_content=test_detail.question.question_content,  # check
                                  answers=test_detail.question.answers))
    return questions


def add_test_detail(test_id, request, db: Session):
    request_set = set(request)
    for j in range(len(request)):
        i = request[j]
        if i in request[j+1:]:
            continue
        question = db.query(models.Question).filter_by(question_id=i).first()
        if not question:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Question in line {j+1} is not found")
        new_test_detail = db.query(models.QuestionTest).filter_by(test_id=test_id,
                                                                  question_id=question.id).first()
        if new_test_detail:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Question in line {j+1} already exists")

        try:
            new_test_detail = models.QuestionTest(test_id=test_id, question_id=question.id)
            db.add(new_test_detail)
        except:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'Add test detail failed in line {j+1}')

    db.commit()
    if len(request) != len(request_set):
        return  {
            'status_code': status.HTTP_207_MULTI_STATUS,
            #detail say: some question duplicated are migrated automatically

            'detail': 'Some duplicate questions have been merged automatically.'
        }
    return {
        'status_code': status.HTTP_201_CREATED,
        'detail': 'Add test detail success'
    }

def delete_test_detail(test_id, question_id, db: Session):
    test_detail = db.query(models.QuestionTest).filter_by(test_id=test_id,
                                                          question_id=question_id).first()
    if not test_detail:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Test {test_id} does not have question {question_id}")
    db.delete(test_detail)
    db.commit()
    return


def get_about_test(test_id: int, db: Session):
    test_details = db.query(models.QuestionTest).filter_by(test_id=test_id).all()
    if not test_details:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Test detail with id {test_id} not found")
    test = test_details[0].test
    data = {'test_id': test.id, 'test_name': test.test_name, 'start_time': test.start_time, 'end_time': test.end_time,
            'duration': test.duration, 'questions': []}
    for i in test_details:
        question = {'question_id': i.question.id, 'question_content': i.question.question_content, 'answers': []}
        for j in i.question.answers:
            question['answers'].append({'answer_id': j.id, 'answer_content': j.answer_content})
        data['questions'].append(question)
    return data
