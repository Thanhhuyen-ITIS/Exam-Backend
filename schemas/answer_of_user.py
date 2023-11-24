from datetime import datetime
from typing import Union

from pydantic import BaseModel

from schemas.answer import AnswerForUser
from schemas.question import Question


class AnswerOfUserBase(BaseModel):
    id: Union[int, None] = None
    question: Question
    answer: list[AnswerForUser] = []
    is_correct: bool

    class Config:
        orm_mode = True

class AnswerOfQuestion(BaseModel):
    question_id: int
    answer: list[AnswerForUser]


class RequestAnswersOfUser(BaseModel):
    result_id: int
    end_time: datetime
    answers: list[AnswerOfQuestion]


    class Config:
        orm_mode = True


