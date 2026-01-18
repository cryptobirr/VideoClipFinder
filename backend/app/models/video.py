"""Video model"""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP, Integer, String, Text, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Video(Base):
    """Video metadata"""

    __tablename__ = "videos"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    title: Mapped[str] = mapped_column(String(500), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(2000))
    source_platform: Mapped[str | None] = mapped_column(String(50))
    creator: Mapped[str | None] = mapped_column(String(200))
    creator_id: Mapped[str | None] = mapped_column(String(200))
    duration_seconds: Mapped[int | None] = mapped_column(Integer)
    published_at: Mapped[datetime | None] = mapped_column(TIMESTAMP(timezone=True))
    thumbnail_url: Mapped[str | None] = mapped_column(String(2000))

    # Aggregated stats
    moment_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_virality_score: Mapped[float] = mapped_column(default=0.0)
    top_tags: Mapped[dict] = mapped_column(JSONB, default=dict)

    # Metadata
    metadata: Mapped[dict] = mapped_column(JSONB, default=dict)
    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    # Relationships
    transcript: Mapped["Transcript"] = relationship(
        "Transcript", back_populates="video", uselist=False, cascade="all, delete-orphan"
    )
    moments: Mapped[list["Moment"]] = relationship(
        "Moment", back_populates="video", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Video(id={self.id}, title={self.title})>"
