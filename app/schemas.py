from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, conint

class PostBase (BaseModel):
    title: str
    content:str
    published: bool = True

class PostCreate(PostBase):
    pass

class UserResponse(BaseModel):
    id:int
    name:str
    email:EmailStr
    created_at: datetime
    
    class Config:
        #will tell the pydantic model to read the data even  if it's not a dict
        orm_mode = True 


class Post(PostBase):
    id:int
    created_at: datetime
    owner_id:int
    owner:UserResponse

    class Config:
        #will tell the pydantic model to read the data even  if it's not a dict
        orm_mode = True


class PostOut(BaseModel):
    Post:Post
    votes:int 
    class Config:
        #will tell the pydantic model to read the data even  if it's not a dict
        orm_mode = True
    
class UserCreate(BaseModel):
    
    name:str
    email:EmailStr
    password :str = Field(min_length=8)
  


class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

class Token (BaseModel):
    access_token: str
    token_type:str

class TokenData (BaseModel):
    id:Optional[int] =None


class Vote(BaseModel):
    post_id:int
    vote_dir: int = Field(..., ge=0, le=1)
