from typing import Union

from pydantic import BaseModel

class UserBase(BaseModel):
    username: str
class UserCreate(UserBase):
    password: str

class User(UserBase):
    name: Union[None, str] = None
    email: Union[None, str] = None

    class Config:
        orm_mode = True

class TokenData(BaseModel):
    username: str
    role: int

    class Config:
        orm_mode = True