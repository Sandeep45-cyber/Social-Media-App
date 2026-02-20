from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class PostBase(BaseModel):
    title:str
    content:str
    published: Optional[bool] = True


class PostCreate(PostBase):
    pass



class Post(BaseModel):
    id:int
    created_at:datetime
    title:str
    content:str
    published:bool

    model_config = ConfigDict(from_attributes=True)
