from fastapi import HTTPException
from sqlalchemy.orm import Session

import models
from schemas.answer import Answer


def add_answer(question_id, request: Answer, db: Session):
    new_answer = models.Answer(question_id=question_id, answer_content=request.answer_content,
                               is_correct_answer=request.is_correct_answer)
    db.add(new_answer)
    db.commit()
    db.refresh(new_answer)
    return new_answer


def add_answers(request: list[Answer], db: Session, question_id: int):
    for answer in request:
        new_answer = models.Answer(question_id=question_id, answer_content=answer.answer_content,
                                   is_correct_answer=answer.is_correct_answer)
        db.add(new_answer)
    db.commit()
    return 'Add success'


# get answer by question_id
def get_answer_by_question_id(question_id, db):
    return db.query(Answer).filter_by(question_id=question_id).all()


def delete_answer(id, db):
    db.delete(db.query(models.Answer).filter_by(id=id).first())
    db.commit()
    return 'deleted successfully'


def update_answer(id, request: Answer, db: Session):
    answer = db.query(models.Answer).filter(models.Answer.id == id).first()
    if not answer:
        raise HTTPException(status_code=404, detail="Answer not found")
    answer.answer_content = request.answer_content
    answer.is_correct_answer = request.is_correct_answer
    db.commit()
    db.refresh(answer)
    return 'Update success'

