from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ReplyBase(BaseModel):
    author: str
    role: str
    content: str

class ReplyCreate(ReplyBase):
    pass

class ReplyUpdate(BaseModel):
    content: Optional[str] = None

class ReplyOut(ReplyBase):
    id: int
    post_id: int
    timestamp: datetime

    class Config:
        from_attributes = True
