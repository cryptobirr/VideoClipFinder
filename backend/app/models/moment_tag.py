"""Moment-Tag junction model"""
from datetime import datetime
from uuid import UUID, uuid4

from sqlalchemy import TIMESTAMP, Float, ForeignKey, Text, func
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class MomentTag(Base):
    """Many-to-many relationship between moments and tags"""

    __tablename__ = "moment_tags"

    id: Mapped[UUID] = mapped_column(PGUUID(as_uuid=True), primary_key=True, default=uuid4)
    moment_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("moments.id", ondelete="CASCADE"), nullable=False
    )
    tag_id: Mapped[UUID] = mapped_column(
        PGUUID(as_uuid=True), ForeignKey("tags.id", ondelete="CASCADE"), nullable=False
    )

    # Confidence and context
    confidence: Mapped[float] = mapped_column(Float, default=1.0)
    context: Mapped[str | None] = mapped_column(Text)

    created_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True), server_default=func.now()
    )

    # Relationships
    moment: Mapped["Moment"] = relationship("Moment", back_populates="moment_tags")
    tag: Mapped["Tag"] = relationship("Tag", back_populates="moment_tags")

    def __repr__(self) -> str:
        return f"<MomentTag(moment_id={self.moment_id}, tag_id={self.tag_id})>"
