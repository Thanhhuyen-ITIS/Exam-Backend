from typing import Union

from pydantic import BaseModel

from schemas.answer import Answer, AnswerForUser


class QuestionBase(BaseModel):
    id: Union[int, None] = None
    question_id: Union[str, None] = None
    question_content: str

    class Config:
        orm_mode = True

class QuestionForUser(QuestionBase):
    answers: list[AnswerForUser]

    class Config:
        orm_mode = True

class Question(QuestionBase):
    answers: list[Answer] = []

    class Config:
        orm_mode = True
