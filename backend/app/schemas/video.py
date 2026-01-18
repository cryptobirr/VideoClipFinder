"""Video schemas"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class VideoBase(BaseModel):
    """Base video fields"""

    title: str = Field(..., max_length=500)
    source_url: str | None = Field(None, max_length=2000)
    source_platform: str | None = Field(None, max_length=50)
    creator: str | None = Field(None, max_length=200)
    creator_id: str | None = Field(None, max_length=200)
    duration_seconds: int | None = None
    published_at: datetime | None = None
    thumbnail_url: str | None = Field(None, max_length=2000)
    metadata: dict = Field(default_factory=dict)


class VideoCreate(VideoBase):
    """Create video request"""

    pass


class VideoUpdate(BaseModel):
    """Update video request"""

    title: str | None = None
    source_url: str | None = None
    creator: str | None = None
    metadata: dict | None = None


class Video(VideoBase):
    """Video response"""

    id: UUID
    moment_count: int = 0
    avg_virality_score: float = 0.0
    top_tags: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class VideoDetail(Video):
    """Video with transcript and moments"""

    transcript: "Transcript | None" = None
    moments: list["Moment"] = Field(default_factory=list)


class VideoList(BaseModel):
    """Paginated video list"""

    videos: list[Video]
    total: int
    page: int
    page_size: int
    total_pages: int


# Forward references
from app.schemas.moment import Moment
from app.schemas.transcript import Transcript

VideoDetail.model_rebuild()
