from pydantic import BaseModel, EmailStr, Field
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(..., max_length=72)
    name: Optional[str] = None
    role: Optional[int] = 0

class UserOut(BaseModel):
    id: int
    email: EmailStr
    name: Optional[str] = None
    role: int

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
