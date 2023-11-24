from typing import Union

from pydantic import BaseModel

from schemas.question import QuestionForUser


class TestDetailCreate(BaseModel):
    id: Union[int, None] = None
    test_id: int
    question_id: int

    class Config:
        orm_mode = True

class TestDetail(BaseModel):
    id: Union[int, None] = None
    question: QuestionForUser

    class Config:
        orm_mode = True


