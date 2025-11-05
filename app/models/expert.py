from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func
from app.db.database import Base


class Expert(Base):
    __tablename__ = "experts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    specialty = Column(String, nullable=True)
    institution = Column(String, nullable=True)
    expertise = Column(JSON, default=list)
    bio = Column(Text, nullable=True)
    education = Column(JSON, default=list)
    publications = Column(Integer, default=0)
    contact = Column(JSON, default=dict)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


