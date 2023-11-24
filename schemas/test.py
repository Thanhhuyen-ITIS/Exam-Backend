from datetime import datetime
from typing import Union

from pydantic import BaseModel

from schemas.test_detail import TestDetail

class TestBase(BaseModel):
    id: Union[int, None] = None
    test_name: str
    start_time: datetime
    end_time: datetime
    duration: int
    permission_review: bool = False

    class Config:
        orm_mode = True

class ResponseTestInforForUser(TestBase):

    status: Union[str, None] = None
    is_start: Union[bool, None] = None

    class Config:
        orm_mode = True
class Test(TestBase):

    status: Union[str, None] = None
    is_start: Union[bool, None] = None

    question_tests: list[TestDetail] = []
    class Config:
        orm_mode = True

class TestCreate(TestBase):
    topic_id: int
    limit: Union[int, None] = None
    class Config:
        orm_mode = True