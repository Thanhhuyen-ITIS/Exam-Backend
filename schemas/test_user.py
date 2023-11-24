from pydantic import BaseModel


class TestUserCreate(BaseModel):
    test_id: int
    username: str

    class Config():
        orm_mode = True