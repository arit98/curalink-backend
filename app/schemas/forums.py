from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ForumPostBase(BaseModel):
    title: str
    author: str
    role: str
    category_id: int
    replies: Optional[int] = 0
    preview: Optional[str] = None

class ForumPostCreate(ForumPostBase):
    pass

class ForumPostUpdate(BaseModel):
    title: Optional[str] = None
    author: Optional[str] = None
    role: Optional[str] = None
    category_id: Optional[int] = None
    replies: Optional[int] = None
    preview: Optional[str] = None

class ForumPostOut(ForumPostBase):
    id: int
    timestamp: datetime

    class Config:
        from_attributes = True
