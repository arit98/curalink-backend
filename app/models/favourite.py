from sqlalchemy import Column, Integer, ForeignKey, String, DateTime, func, UniqueConstraint
from app.db.database import Base


class Favourite(Base):
    __tablename__ = "favourites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    content_type = Column(String, nullable=False)  # trial|expert|publication
    content_id = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    __table_args__ = (UniqueConstraint("user_id", "content_type", "content_id", name="uix_user_content"),)