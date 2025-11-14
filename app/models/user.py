from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.db.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    hashed_password = Column(String, nullable=False)
    name = Column(String, nullable=True)
    role = Column(Integer, default=0)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    has_onboarded = Column(Boolean, default=False)

    # Relationships for onboarding data
    researcher_profile = relationship(
        "ResearcherProfile", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
    patient_profile = relationship(
        "PatientProfile", uselist=False, back_populates="user", cascade="all, delete-orphan"
    )
