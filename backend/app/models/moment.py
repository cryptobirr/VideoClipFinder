"""Moment model"""
from datetime import datetime
from uuid import UUID, uuid4

from pgvector.sqlalchemy import Vector
from sqlalchemy import TIMESTAMP, Float, ForeignKey, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Moment(Base):
    """Tagged moment from video"""

    __tablename__ = "moments"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    video_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("videos.id", ondelete="CASCADE"), nullable=False
    )

    # Timing
    start_time: Mapped[float] = mapped_column(Float, nullable=False)
    end_time: Mapped[float] = mapped_column(Float, nullable=False)

    # Content
    summary: Mapped[str] = mapped_column(Text, nullable=False)
    transcript_excerpt: Mapped[str | None] = mapped_column(Text)

    # Virality scores (0-10)
    virality_hook_strength: Mapped[float] = mapped_column(Float, default=0.0)
    virality_shareability: Mapped[float] = mapped_column(Float, default=0.0)
    virality_clip_independence: Mapped[float] = mapped_column(Float, default=0.0)
    virality_emotional_intensity: Mapped[float] = mapped_column(Float, default=0.0)

    # Platform fit scores (0-10)
    platform_tiktok: Mapped[float] = mapped_column(Float, default=0.0)
    platform_youtube_shorts: Mapped[float] = mapped_column(Float, default=0.0)
    platform_instagram_reels: Mapped[float] = mapped_column(Float, default=0.0)
    platform_twitter: Mapped[float] = mapped_column(Float, default=0.0)

    # Clip metadata
    suggested_clip_start: Mapped[float | None] = mapped_column(Float)
    suggested_clip_end: Mapped[float | None] = mapped_column(Float)
    suggested_hook_lines: Mapped[dict] = mapped_column(JSONB, default=dict)
    requires_context: Mapped[str] = mapped_column(String(20), default="none")

    # Embedding for semantic search (1536 dimensions for OpenAI)
    embedding: Mapped[Vector] = mapped_column(Vector(1536), nullable=True)

    # Extended metadata
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Processing
    analyzed_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    analysis_version: Mapped[str | None] = mapped_column(String(20))

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    video: Mapped["Video"] = relationship("Video", back_populates="moments")
    moment_tags: Mapped[list["MomentTag"]] = relationship(
        "MomentTag", back_populates="moment", cascade="all, delete-orphan"
    )

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

    def __repr__(self) -> str:
        return f"<Moment(id={self.id}, video_id={self.video_id}, virality={self.virality_overall:.1f})>"
