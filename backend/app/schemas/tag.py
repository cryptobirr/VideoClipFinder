"""Tag schemas"""
from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class TagDimensionBase(BaseModel):
    """Base tag dimension fields"""

    name: str = Field(..., max_length=100)
    description: str | None = None
    color: str | None = Field(None, max_length=7)
    icon: str | None = Field(None, max_length=50)
    sort_order: int = 0


class TagDimension(TagDimensionBase):
    """Tag dimension response"""

    id: UUID

    model_config = {"from_attributes": True}


class TagBase(BaseModel):
    """Base tag fields"""

    name: str = Field(..., max_length=100)
    slug: str = Field(..., max_length=100)
    description: str | None = None
    color: str | None = Field(None, max_length=7)
    icon: str | None = Field(None, max_length=50)


class Tag(TagBase):
    """Tag response"""

    id: UUID
    dimension_id: UUID | None
    usage_count: int = 0
    created_at: datetime

    model_config = {"from_attributes": True}


class TagWithDimension(Tag):
    """Tag with dimension info"""

    dimension: TagDimension | None


class TagStats(BaseModel):
    """Tag statistics"""

    tag: TagWithDimension
    usage_count: int
    avg_virality: float
    video_count: int


class TagsByDimension(BaseModel):
    """Tags grouped by dimension"""

    dimension: TagDimension
    tags: list[Tag]


class TagAutocomplete(BaseModel):
    """Tag autocomplete result"""

    slug: str
    name: str
    dimension: str | None
