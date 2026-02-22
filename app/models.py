"""SQLAlchemy ORM models for persisted application data."""

from .database import Base
from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String, func, text


class Post(Base):
    """Database table mapping for social posts."""

    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default=text("TRUE"), nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
