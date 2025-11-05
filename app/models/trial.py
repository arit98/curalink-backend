from sqlalchemy import Column, Integer, String, Text, Boolean, JSON
from app.db.database import Base


class Trial(Base):
    __tablename__ = "trials"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    phase = Column(String, nullable=True)
    location = Column(String, nullable=True)
    summary = Column(Text, nullable=True)
    recruiting = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
    eligibility = Column(JSON, default=list)
    contact = Column(JSON, default=dict)
    institution = Column(String, nullable=True)
    enrollment = Column(String, nullable=True)
    status = Column(String, default="active")
