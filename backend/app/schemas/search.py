"""Search schemas"""
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.moment import MomentWithTags


class TagSearchRequest(BaseModel):
    """Tag-based search request"""

    tags: list[str] = Field(..., min_length=1)  # tag slugs
    operator: str = Field(default="AND", pattern="^(AND|OR)$")
    min_virality: float = Field(default=0.0, ge=0.0, le=10.0)
    video_ids: list[UUID] | None = None
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)


class TagSearchResponse(BaseModel):
    """Tag-based search response"""

    moments: list[MomentWithTags]
    total_count: int
    query_time_ms: float
    page: int
    page_size: int
    total_pages: int


class SemanticSearchRequest(BaseModel):
    """Semantic search request"""

    query: str = Field(..., min_length=1, max_length=500)
    min_similarity: float = Field(default=0.7, ge=0.0, le=1.0)
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)


class PatternDiscoveryRequest(BaseModel):
    """Pattern discovery request"""

    min_occurrences: int = Field(default=5, ge=1)
    min_virality: float = Field(default=0.0, ge=0.0, le=10.0)
    limit: int = Field(default=20, ge=1, le=100)


class SearchPattern(BaseModel):
    """Tag correlation pattern"""

    tag_pattern: list[str]  # tag slugs
    occurrence_count: int
    avg_virality: float
    example_moments: list[MomentWithTags] = Field(default_factory=list)


class PatternDiscoveryResponse(BaseModel):
    """Pattern discovery response"""

    patterns: list[SearchPattern]
    total_patterns: int
    query_time_ms: float


class FullTextSearchRequest(BaseModel):
    """Full-text search request"""

    query: str = Field(..., min_length=1, max_length=500)
    limit: int = Field(default=50, ge=1, le=200)
    offset: int = Field(default=0, ge=0)
