from pydantic import BaseModel
from typing import Optional, List


class PublicationCreate(BaseModel):
    title: str
    authors: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[str] = None
    abstract: Optional[str] = None
    tags: Optional[List[str]] = []
    doi: Optional[str] = None
    fullAbstract: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None


class PublicationOut(BaseModel):
    id: int
    title: str
    authors: Optional[str] = None
    journal: Optional[str] = None
    year: Optional[str] = None
    abstract: Optional[str] = None
    tags: Optional[List[str]] = []
    doi: Optional[str] = None
    fullAbstract: Optional[str] = None
    methodology: Optional[str] = None
    results: Optional[str] = None
    conclusion: Optional[str] = None

    class Config:
        from_attributes = True


