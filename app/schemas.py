from pydantic import BaseModel, EmailStr, conint
from datetime import datetime
from typing import Optional


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserPublic(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class ConfigDict:
        from_attributes = True


class Post(PostBase):
    id: int
    created_at: datetime
    author_id: int
    author: UserPublic

    class ConfigDict:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None


class Vote(BaseModel):
    post_id: int
    vote_dir: conint(ge=0, le=1)


class PostOut(BaseModel):
    Post: Post
    votes: int

    class ConfigDict:
        from_attributes = True


class ChangePassword(BaseModel):
    password: str
    new_password: str
