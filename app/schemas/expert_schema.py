from pydantic import BaseModel, EmailStr
from typing import Optional, List


class Contact(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None


class ExpertCreate(BaseModel):
    name: str
    specialty: Optional[str] = None
    institution: Optional[str] = None
    expertise: Optional[List[str]] = []
    bio: Optional[str] = None
    education: Optional[List[str]] = []
    publications: Optional[int] = 0
    contact: Optional[Contact] = None


class ExpertOut(BaseModel):
    id: int
    name: str
    specialty: Optional[str] = None
    institution: Optional[str] = None
    expertise: Optional[List[str]] = []
    bio: Optional[str] = None
    education: Optional[List[str]] = []
    publications: int
    contact: Optional[Contact] = None

    class Config:
        from_attributes = True


