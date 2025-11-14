from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base

class ResearcherProfile(Base):
    __tablename__ = "researcher_profiles"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    condition = Column(String, nullable=False)
    location = Column(String, nullable=True)
    tags = Column(String, nullable=True)

    user = relationship("User", back_populates="researcher_profile")
