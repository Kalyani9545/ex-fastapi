from pydantic import BaseModel,EmailStr
from datetime import datetime  
from typing import Optional
from pydantic.types import conint


class PostBase(BaseModel):
    title: str 
    content: str 
    published: bool=True
    
class PostCreate(PostBase):
    pass


class userOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode=True


class My_data(PostBase):
    id:int
    created_at:datetime
    owner_id:int
    owner:userOut
    class Config:
        orm_mode=True 


class Vote(BaseModel):
    post_id: int
    dir:conint(le=1)

class PostOut(PostBase):
    Post:My_data
    vote:int

    class Config:
        orm_mode=True


class User(BaseModel):
    email:EmailStr
    password:str


class userLogin(BaseModel):
    email:EmailStr
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]=None


