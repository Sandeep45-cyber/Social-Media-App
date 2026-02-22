"""Pydantic request and response schemas for API payloads."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class PostBase(BaseModel):
    """Shared post payload fields used by create/read operations."""

    title: str
    content: str
    published: Optional[bool] = True


class PostCreate(PostBase):
    """Schema for creating a new post."""


class Post(BaseModel):
    """Schema returned to clients for persisted posts."""

    id: int
    created_at: datetime
    title: str
    content: str
    published: bool

    model_config = ConfigDict(from_attributes=True)
