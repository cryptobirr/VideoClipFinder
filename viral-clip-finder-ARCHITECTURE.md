# Viral Clip Finder - System Architecture

## Overview

An AI-powered system for analyzing video transcripts, tagging moments with rich metadata, and discovering viral clip opportunities through cross-video pattern correlation.

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              VIRAL CLIP FINDER                               │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                              │
│   ┌──────────────┐     ┌──────────────┐     ┌──────────────────────────┐   │
│   │   React UI   │────▶│   FastAPI    │────▶│   PostgreSQL + pgvector  │   │
│   │  (Vite+CN)   │◀────│   Backend    │◀────│   (Supabase/Neon)        │   │
│   └──────────────┘     └──────┬───────┘     └──────────────────────────┘   │
│                               │                                              │
│                         ┌─────▼─────┐                                       │
│                         │  Claude   │                                       │
│                         │   API     │                                       │
│                         └───────────┘                                       │
│                                                                              │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Core Concepts

### 1. Video
A content piece (YouTube video, livestream, etc.) with metadata.

### 2. Transcript
Raw text transcript with timestamps, associated with a video.

### 3. Moment
A tagged segment of a video with:
- Timestamp range (start/end)
- Multiple tags across dimensions
- Virality scores
- Embedding vector for semantic search

### 4. Tag
A label from a controlled taxonomy, categorized by dimension:
- Content type, emotion, interaction, viral markers, etc.

### 5. Tag Correlation
Patterns discovered across many videos:
- "Food reaction + disgust + host_genuine = high viral potential"
- "Doppelganger reveal + crowd_reaction = clip gold"

---

## Data Model

### Entity Relationship Diagram

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   videos    │───────│  transcripts │       │    tags     │
├─────────────┤  1:1  ├──────────────┤       ├─────────────┤
│ id          │       │ id           │       │ id          │
│ title       │       │ video_id     │       │ name        │
│ source_url  │       │ raw_text     │       │ dimension   │
│ creator     │       │ status       │       │ parent_id   │
│ duration    │       │ created_at   │       │ description │
│ metadata    │       └──────────────┘       └─────────────┘
└─────────────┘                                     │
      │                                             │
      │ 1:N                                         │ M:N
      ▼                                             ▼
┌─────────────┐       ┌──────────────────┐  ┌─────────────────┐
│   moments   │───────│  moment_tags     │──│ tag instances   │
├─────────────┤  1:N  ├──────────────────┤  ├─────────────────┤
│ id          │       │ moment_id        │  │ with confidence │
│ video_id    │       │ tag_id           │  │ and context     │
│ start_time  │       │ confidence       │  └─────────────────┘
│ end_time    │       │ context          │
│ summary     │       └──────────────────┘
│ transcript  │
│ virality_*  │       ┌──────────────────┐
│ embedding   │       │ tag_correlations │
│ metadata    │       ├──────────────────┤
└─────────────┘       │ tag_pattern      │
                      │ occurrence_count │
                      │ avg_virality     │
                      │ example_moments  │
                      └──────────────────┘
```

---

## Processing Pipeline

```
┌─────────────────────────────────────────────────────────────────┐
│                     INGESTION PIPELINE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. UPLOAD          2. SEGMENT           3. ANALYZE            │
│  ┌─────────┐        ┌─────────┐         ┌─────────┐           │
│  │ Video + │───────▶│ Split   │────────▶│ Claude  │           │
│  │ Trans.  │        │ into    │  batch  │ tags    │           │
│  └─────────┘        │ chunks  │         │ moments │           │
│                     └─────────┘         └────┬────┘           │
│                                              │                 │
│  4. EMBED           5. STORE            6. INDEX              │
│  ┌─────────┐        ┌─────────┐         ┌─────────┐           │
│  │ Generate│◀───────│ Save    │────────▶│ Update  │           │
│  │ vectors │        │ moments │         │ search  │           │
│  └─────────┘        │ & tags  │         │ indices │           │
│                     └─────────┘         └─────────┘           │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

### Pipeline Details

1. **Upload**: Video metadata + transcript text ingested
2. **Segment**: Transcript split into ~3 minute chunks with overlap
3. **Analyze**: Claude processes each chunk, returns tagged moments
4. **Embed**: Generate embedding vectors for semantic search
5. **Store**: Persist moments, tags, scores to database
6. **Index**: Update full-text and vector search indices

---

## Search Architecture

### Search Types

1. **Tag Search**: Find moments by exact tag match
   - "Find all `crowd_rush` moments"
   
2. **Tag Combination**: Boolean combinations
   - "Find `food_reaction` AND `disgust` moments"
   
3. **Semantic Search**: Vector similarity
   - "Find moments similar to 'streamer tries weird food and hates it'"
   
4. **Pattern Discovery**: Find co-occurring tags
   - "What tags often appear with `milestone_celebration`?"

### Indexing Strategy

```sql
-- Full-text search on moment content
CREATE INDEX idx_moments_fts ON moments USING GIN(to_tsvector('english', summary || ' ' || transcript_excerpt));

-- Vector similarity search
CREATE INDEX idx_moments_embedding ON moments USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Tag lookup
CREATE INDEX idx_moment_tags_tag ON moment_tags(tag_id);
CREATE INDEX idx_moment_tags_moment ON moment_tags(moment_id);

-- Time-based queries
CREATE INDEX idx_moments_video_time ON moments(video_id, start_time);
```

---

## Scale Considerations

### Target Scale
- 10,000+ videos
- 100+ moments per video average
- 1,000,000+ total moments
- 50+ tags per moment average

### Optimizations

1. **Batch Processing**: Process transcripts in parallel chunks
2. **Async Pipeline**: Queue-based processing with workers
3. **Incremental Updates**: Only re-analyze changed content
4. **Materialized Views**: Pre-compute tag correlations
5. **Connection Pooling**: pgBouncer for database connections
6. **Caching**: Redis for frequent tag/pattern queries

### Database Partitioning

```sql
-- Partition moments by video for efficient queries
CREATE TABLE moments (
    ...
) PARTITION BY HASH (video_id);

-- Create partitions
CREATE TABLE moments_0 PARTITION OF moments FOR VALUES WITH (MODULUS 4, REMAINDER 0);
CREATE TABLE moments_1 PARTITION OF moments FOR VALUES WITH (MODULUS 4, REMAINDER 1);
-- etc.
```

---

## API Design

### Endpoints

```
Videos
  POST   /api/videos                    # Create video + transcript
  GET    /api/videos                    # List videos (paginated)
  GET    /api/videos/:id                # Get video details
  POST   /api/videos/:id/analyze        # Trigger analysis
  GET    /api/videos/:id/moments        # Get video moments

Moments  
  GET    /api/moments                   # Search moments
  GET    /api/moments/:id               # Get moment details
  
Tags
  GET    /api/tags                      # List all tags
  GET    /api/tags/:id/moments          # Get moments for tag
  
Search
  POST   /api/search/tags               # Tag-based search
  POST   /api/search/semantic           # Vector similarity search
  POST   /api/search/patterns           # Find tag patterns
  
Analytics
  GET    /api/analytics/correlations    # Tag co-occurrence stats
  GET    /api/analytics/top-moments     # Highest virality moments
```

---

## Technology Stack

| Component | Technology | Rationale |
|-----------|------------|-----------|
| Frontend | React + Vite + shadcn/ui | Fast dev, great components |
| Backend | Python FastAPI | Async, fast, great typing |
| Database | PostgreSQL + pgvector | Relational + vector search |
| AI | Claude API | Best-in-class analysis |
| Embeddings | Voyage AI / OpenAI | High quality vectors |
| Queue | Redis + Celery | Background job processing |
| Hosting | Supabase / Railway | Easy managed Postgres |

---

## Directory Structure

```
viral-clip-finder/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py              # FastAPI app
│   │   ├── config.py            # Settings
│   │   ├── database.py          # DB connection
│   │   ├── models/              # SQLAlchemy models
│   │   │   ├── video.py
│   │   │   ├── moment.py
│   │   │   └── tag.py
│   │   ├── schemas/             # Pydantic schemas
│   │   ├── api/                 # Route handlers
│   │   │   ├── videos.py
│   │   │   ├── moments.py
│   │   │   └── search.py
│   │   ├── services/            # Business logic
│   │   │   ├── analyzer.py      # AI analysis
│   │   │   ├── embeddings.py    # Vector generation
│   │   │   └── correlations.py  # Pattern discovery
│   │   └── prompts/             # AI prompt templates
│   │       └── moment_tagger.py
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── components/
│   │   ├── pages/
│   │   └── lib/
│   ├── package.json
│   └── vite.config.js
├── database/
│   ├── migrations/
│   └── schema.sql
└── docker-compose.yml
```
