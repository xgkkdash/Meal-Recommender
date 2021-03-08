from pydantic import BaseModel


class UserBase(BaseModel):
    account_id: str
    password: str
    email: str

    name: str = None
    age: int = None
    gender: str = None
    height: int = None
    weight: int = None


class UserCreate(UserBase):
    pass


class User(UserBase):

    class Config:
        orm_mode = True


