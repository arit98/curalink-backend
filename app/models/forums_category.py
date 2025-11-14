from sqlalchemy import Column, Integer, String
from app.db.database import Base

class ForumCategory(Base):
    __tablename__ = "forum_categories"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, nullable=False)