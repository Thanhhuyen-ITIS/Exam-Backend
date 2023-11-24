from datetime import datetime
from typing import Union

from pydantic import BaseModel


class TopicBase(BaseModel):
    topic_name: Union[str, None] = None
    topic_image: Union[None, str] = None

class Topic(TopicBase):
    id: Union[int, None] = None

    class Config:
        orm_mode = True

class TopicShow(Topic):
    create_time: Union[datetime, None] = None

    class Config:
        orm_mode = True