from pydantic import BaseModel
from typing import Optional, List


class Contact(BaseModel):
    name: str
    email: str
    phone: Optional[str] = None


class TrialCreate(BaseModel):
    title: str
    phase: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    recruiting: Optional[bool] = True
    description: Optional[str] = None
    eligibility: Optional[List[str]] = []
    contact: Optional[Contact] = None
    institution: Optional[str] = None
    enrollment: Optional[str] = None
    status: Optional[str] = "active"


class TrialOut(BaseModel):
    id: int
    title: str
    phase: Optional[str] = None
    location: Optional[str] = None
    summary: Optional[str] = None
    recruiting: bool
    description: Optional[str] = None
    eligibility: Optional[List[str]] = []
    contact: Optional[Contact] = None
    institution: Optional[str] = None
    enrollment: Optional[str] = None
    status: str

    class Config:
        from_attributes = True
