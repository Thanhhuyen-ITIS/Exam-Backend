from fastapi import HTTPException
from sqlalchemy import not_
from sqlalchemy.orm import Session

import models
from repository import answer_repo
from schemas.question import Question


def add_question(request: Question, db: Session):
    new_question = db.query(models.Question).filter(
        models.Question.question_content == request.question_content or models.Question.question_id == request.question_id).first()
    if new_question:
        raise HTTPException(status_code=400, detail="Question already exists")
    new_question = models.Question(question_id=request.question_id, question_content=request.question_content)
    db.add(new_question)
    db.commit()
    db.refresh(new_question)
    answer_repo.add_answers(request.answers, db, new_question.id)

    return 'Add question success'


def delete_question(id: int, db: Session):
    question = db.query(models.Question).filter(models.Question.id == id).first()
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")
    db.delete(question)
    db.commit()
    return 'Delete success'


def update_question(id: int, request: Question, db: Session):
    question = db.query(models.Question).filter(models.Question.id == id).first()
    answer_db = question.answers
    if not question:
        raise HTTPException(status_code=404, detail="Question not found")

    if db.query(models.Question).filter(models.Question.question_content == request.question_content,
                                        models.Question.id != id).count() > 0:
        raise HTTPException(status_code=400, detail="Question already exists")

    try:
        question.question_id = request.question_id
        question.question_content = request.question_content

        for answer in request.answers:
            if answer.id == 0:
                answer_repo.add_answer(question.id, answer, db)
            else:
                answer_repo.update_answer(answer.id, answer, db)

        for answer in answer_db:
            if answer.id not in [ans.id for ans in request.answers]:
                answer_repo.delete_answer(answer.id, db)
        db.commit()
        db.refresh(question)
    except:
        db.rollback()
        raise HTTPException(status_code=400, detail="Update failed")
    return 'Update success'


def get_questions(db: Session):
    questions_db = db.query(models.Question).all()

    return questions_db
