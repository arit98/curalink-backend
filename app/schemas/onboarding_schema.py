from pydantic import BaseModel
from typing import Optional, List

class ResearcherProfileCreate(BaseModel):
    condition: str
    location: Optional[str] = None
    tags: Optional[List[str]] = []

class ResearcherProfileUpdate(BaseModel):
    condition: Optional[str] = None
    location: Optional[str] = None
    tags: Optional[List[str]] = None

class PatientProfileCreate(BaseModel):
    condition: str
    location: Optional[str] = None

class PatientProfileUpdate(BaseModel):
    condition: Optional[str] = None
    location: Optional[str] = None