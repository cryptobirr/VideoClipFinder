"""Transcript schemas"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TranscriptBase(BaseModel):
    """Base transcript fields"""

    raw_text: str = Field(..., min_length=1)
    language: str = Field(default="en", max_length=10)
    source: str | None = Field(None, max_length=50)


class TranscriptCreate(TranscriptBase):
    """Create transcript request"""

    video_id: UUID


class Transcript(TranscriptBase):
    """Transcript response"""

    id: UUID
    video_id: UUID
    word_count: int | None = None
    status: str = "pending"
    processed_at: datetime | None = None
    error_message: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}
