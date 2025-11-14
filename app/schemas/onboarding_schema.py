from pydantic import BaseModel
from typing import Optional, List

class ResearcherProfileCreate(BaseModel):
    condition: str
    location: Optional[str] = None
    tags: Optional[List[str]] = []

class PatientProfileCreate(BaseModel):
    condition: str
    location: Optional[str] = None