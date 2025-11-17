from sqlalchemy import Column, Integer, String, Text, JSON, DateTime, func, ForeignKey
from app.db.database import Base


class Publication(Base):
    __tablename__ = "publications"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    authors = Column(String, nullable=True)
    journal = Column(String, nullable=True)
    year = Column(String, nullable=True)
    abstract = Column(Text, nullable=True)
    tags = Column(JSON, default=list)
    doi = Column(String, nullable=True)
    fullAbstract = Column(Text, nullable=True)
    methodology = Column(Text, nullable=True)
    results = Column(Text, nullable=True)
    conclusion = Column(Text, nullable=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())


