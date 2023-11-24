from datetime import datetime
from typing import Union

from pydantic import BaseModel

from schemas.answer_of_user import AnswerOfUserBase
from schemas.test import Test, TestBase
from schemas.user import User


class ResultCreate(BaseModel):
    test_id: int

    class Config:
        orm_mode = True


class ResultBase(BaseModel):
    id: Union[int, None] = None
    user: User = None
    test: TestBase = None
    start_time: datetime
    class Config:
        orm_mode = True

class ResponseResultCreate(BaseModel):
    id: int
    test: Test
    start_time: datetime
    end_time: Union[datetime, None] = None
    score: Union[float, None] = None

    class Config:
        orm_mode = True

class ResponseResultDetail(ResultBase):
    completion_time: int
    score: Union[float, None] = None
    answer_of_users: list[AnswerOfUserBase] = []

    class Config:
        orm_mode = True


class Result(BaseModel):
    user: User = None
    id: Union[int, None] = None
    completion_time: Union[int, None] = None
    score: Union[float, None] = None
