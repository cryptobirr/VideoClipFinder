"""Moment schemas"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class ViralityScores(BaseModel):
    """Virality score breakdown"""

    hook_strength: float = Field(default=0.0, ge=0.0, le=10.0)
    shareability: float = Field(default=0.0, ge=0.0, le=10.0)
    clip_independence: float = Field(default=0.0, ge=0.0, le=10.0)
    emotional_intensity: float = Field(default=0.0, ge=0.0, le=10.0)


class PlatformScores(BaseModel):
    """Platform fit scores"""

    tiktok: float = Field(default=0.0, ge=0.0, le=10.0)
    youtube_shorts: float = Field(default=0.0, ge=0.0, le=10.0)
    instagram_reels: float = Field(default=0.0, ge=0.0, le=10.0)
    twitter: float = Field(default=0.0, ge=0.0, le=10.0)


class MomentBase(BaseModel):
    """Base moment fields"""

    start_time: float = Field(..., ge=0.0)
    end_time: float = Field(..., ge=0.0)
    summary: str = Field(..., min_length=1)
    transcript_excerpt: str | None = None
    requires_context: str = Field(default="none", max_length=20)


class MomentCreate(MomentBase):
    """Create moment request"""

    video_id: UUID
    virality_scores: ViralityScores
    platform_scores: PlatformScores
    suggested_clip_start: float | None = None
    suggested_clip_end: float | None = None
    suggested_hook_lines: list[str] = Field(default_factory=list)
    tags: dict[str, list[str]] = Field(
        default_factory=dict
    )  # dimension -> [tag slugs]
    metadata: dict = Field(default_factory=dict)


class Moment(MomentBase):
    """Moment response"""

    id: UUID
    video_id: UUID

    # Virality scores
    virality_hook_strength: float
    virality_shareability: float
    virality_clip_independence: float
    virality_emotional_intensity: float

    # Platform scores
    platform_tiktok: float
    platform_youtube_shorts: float
    platform_instagram_reels: float
    platform_twitter: float

    # Clip metadata
    suggested_clip_start: float | None
    suggested_clip_end: float | None
    suggested_hook_lines: dict = Field(default_factory=dict)

    metadata: dict = Field(default_factory=dict)
    created_at: datetime
    updated_at: datetime

    @property
    def virality_overall(self) -> float:
        """Calculate overall virality score"""
        return (
            self.virality_hook_strength
            + self.virality_shareability
            + self.virality_clip_independence
            + self.virality_emotional_intensity
        ) / 4

    @property
    def duration_seconds(self) -> float:
        """Calculate moment duration"""
        return self.end_time - self.start_time

    model_config = {"from_attributes": True}


class MomentWithTags(Moment):
    """Moment with associated tags"""

    tags: dict[str, list["TagWithDimension"]] = Field(default_factory=dict)


class MomentDetail(MomentWithTags):
    """Moment with video details"""

    video_title: str
    video_creator: str | None


class MomentList(BaseModel):
    """Paginated moment list"""

    moments: list[MomentWithTags]
    total: int
    page: int
    page_size: int
    total_pages: int


# Forward references
from app.schemas.tag import TagWithDimension

MomentWithTags.model_rebuild()
