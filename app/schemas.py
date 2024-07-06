from pydantic import BaseModel, EmailStr, ConfigDict    # this validates the request sent by the user
from datetime import datetime
from typing import Optional

from pydantic.types import conint

#this class is validating the schema sended by the user.
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = None  # this will to equal to None if the user do not provide it in input.


class PostCreate(PostBase):
    pass


class UserResponse(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str

# schemas of response send after request 
class PostResponse(PostBase):
    id: int
    created_at: datetime
    user_id: int
    user: UserResponse
    # inheriting title, content, published from PostBase



class PostWithVoteResponse(BaseModel):
    Post: PostResponse
    votes: int


    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    email: EmailStr    #checks that the entered email is a valid email or not.
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenDate(BaseModel):
    model_config = ConfigDict(coerce_numbers_to_str=True)   # do not remove this line it is very important.
    id: Optional[str] = None


class vote(BaseModel):
    post_id: int
    dir: int