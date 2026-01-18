"""Tag correlation model"""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import ARRAY, TIMESTAMP, Float, Integer, String, func
from sqlalchemy.dialects.postgresql import JSONB, UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class TagCorrelation(Base):
    """Tag co-occurrence patterns"""

    __tablename__ = "tag_correlations"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)

    # Tag pattern
    tag_pattern: Mapped[list[UUID]] = mapped_column(ARRAY(PGUUID(as_uuid=True)), nullable=False)
    tag_pattern_slugs: Mapped[list[str]] = mapped_column(ARRAY(String(100)), nullable=False)

    # Stats
    occurrence_count: Mapped[int] = mapped_column(Integer, default=0)
    avg_virality_score: Mapped[float] = mapped_column(Float, default=0.0)

    # Sample moments
    example_moment_ids: Mapped[list[UUID]] = mapped_column(
        ARRAY(PGUUID(as_uuid=True)), default=list
    )

    # Pattern metadata
    pattern_hash: Mapped[str | None] = mapped_column(String(64), unique=True)

    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now()
    )

    def __repr__(self) -> str:
        return f"<TagCorrelation(pattern={self.tag_pattern_slugs}, count={self.occurrence_count})>"
