from typing import Union

from pydantic import BaseModel


class UserBase(BaseModel):
    name: str


class UserCreate(UserBase):
    password: str


class UserLogin(UserCreate):
    ...


class UserUpdate(BaseModel):
    name: Union[str, None] = None


class User(UserBase):
    id: int

    class Config:
        orm_mode = True
