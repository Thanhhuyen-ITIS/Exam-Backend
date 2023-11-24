from typing import Union

from pydantic import BaseModel


class AnswerBase(BaseModel):
    id: Union[int, None] = None
    question_id: int
    answer_content: str


# respones for user
class AnswerForUser(BaseModel):
    id: Union[int, None] = None
    answer_content: str
    is_selected: bool = False

    class Config:
        orm_mode = True


class Answer(BaseModel):
    id: Union[int, None] = None
    answer_content: str
    is_correct_answer: bool

    class Config:
        orm_mode = True
