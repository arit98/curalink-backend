from sqlalchemy import Column, Integer, String, ForeignKey, Text, DateTime
from app.db.database import Base
from datetime import datetime
from app.models.forums_category import ForumCategory
from sqlalchemy.orm import relationship

class ForumPost(Base):
    __tablename__ = "forum_posts"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    author = Column(String)
    role = Column(String)
    category_id = Column(Integer, ForeignKey("forum_categories.id"))
    replies = Column(Integer, default=0)
    preview = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

    category = relationship("ForumCategory", backref="posts")
