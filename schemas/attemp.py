from typing import Union

from pydantic import BaseModel


class AttempCreate(BaseModel):
    test_id: int

class Attemp(AttempCreate):
    id: Union[int, None] = None
    user_id: str

    class Config:
        orm_mode = True