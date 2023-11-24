from typing import Union

from pydantic import BaseModel


class TopicDetail(BaseModel):
    id: Union[int, None] = None
    topic_id: int
    test_id: int

    class Config:
        orm_mode = True

