from typing import List, Optional

from pydantic import BaseModel

class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    pass


class CommentUpdate(CommentBase):
    id: int


class Comment(CommentBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    email: str


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]


class User(UserBase):
    id: int
    comments: List[Comment]

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str


class Animal(BaseModel):
    name: str
    latin_name: str