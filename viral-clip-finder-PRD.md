# Viral Clip Finder - Product Requirements Document

**Version:** 1.0  
**Date:** January 18, 2026  
**Status:** MVP Design Complete

---

## 1. Executive Summary

Viral Clip Finder is an AI-powered system that analyzes video transcripts to identify, tag, and score potential viral moments. The magic happens at scale: by correlating tagged moments across thousands of videos, the system discovers patterns that predict viral success.

**Core Value Proposition:** Transform hours of video content into a searchable database of viral-ready clips, with AI-generated tags that enable pattern discovery across your entire content library.

---

## 2. Problem Statement

Content creators and clip channels face a critical challenge: identifying the best moments from long-form content (livestreams, podcasts, interviews) to repurpose as short-form viral clips. Current approaches are:

- **Manual:** Editors watch hours of content, relying on intuition
- **Slow:** A 4-hour stream takes 4+ hours to review
- **Inconsistent:** Different editors tag differently, preventing pattern analysis
- **Isolated:** No way to correlate what works across many videos

**The Opportunity:** With consistent AI tagging across thousands of videos, we can discover which tag combinations correlate with viral success—turning clip selection from art into science.

---

## 3. Goals & Success Metrics

### Primary Goals

| Goal | Metric | Target |
|------|--------|--------|
| Speed | Time to analyze 4-hour video | < 10 minutes |
| Coverage | Moments identified per hour of content | 20-40 moments |
| Accuracy | Tags correctly applied (human review) | > 85% |
| Discovery | Actionable patterns found | 50+ patterns |
| Scale | Videos supported | 10,000+ |

### Secondary Goals

- Enable semantic search ("find moments like X")
- Platform-specific clip recommendations (TikTok vs YouTube Shorts)
- Reduce time-to-clip by 80%

---

## 4. User Stories

### Content Creator
> "As a creator with 100+ hours of livestream archives, I want to quickly find my best moments so I can create clips without rewatching everything."

### Clip Channel Operator
> "As someone who clips multiple creators, I want to search across all my analyzed videos by tag combinations to find patterns that work."

### Content Strategist
> "As a strategist, I want to understand which types of moments perform best so I can guide creators on what to emphasize."

---

## 5. Functional Requirements

### 5.1 Video & Transcript Management

| ID | Requirement | Priority |
|----|-------------|----------|
| F1.1 | Upload video metadata (title, creator, duration, URL) | P0 |
| F1.2 | Upload/paste transcript with timestamps | P0 |
| F1.3 | Parse timestamps in multiple formats (0:07, 12:34, 1:23:45) | P0 |
| F1.4 | List all videos with moment counts and avg virality | P0 |
| F1.5 | Delete video and all associated moments | P1 |
| F1.6 | Auto-fetch YouTube transcript via API | P2 |

### 5.2 AI Analysis

| ID | Requirement | Priority |
|----|-------------|----------|
| F2.1 | Chunk transcript into ~3 minute segments with overlap | P0 |
| F2.2 | Process chunks through Claude AI with tagging prompt | P0 |
| F2.3 | Extract moments with start/end timestamps | P0 |
| F2.4 | Apply tags across 6 dimensions per moment | P0 |
| F2.5 | Generate virality scores (hook, shareability, independence, emotion) | P0 |
| F2.6 | Generate platform-specific scores (TikTok, Shorts, Reels, Twitter) | P0 |
| F2.7 | Extract suggested hook lines for clips | P1 |
| F2.8 | Indicate context requirements (standalone vs needs setup) | P1 |
| F2.9 | Parallel processing with concurrency limits | P0 |
| F2.10 | Background job queue for analysis | P1 |

### 5.3 Search & Discovery

| ID | Requirement | Priority |
|----|-------------|----------|
| F3.1 | Search by single tag | P0 |
| F3.2 | Search by tag combination with AND/OR operators | P0 |
| F3.3 | Filter by minimum virality score | P0 |
| F3.4 | Filter by specific video(s) | P1 |
| F3.5 | Semantic search by natural language description | P1 |
| F3.6 | Full-text search on transcript content | P1 |
| F3.7 | Get related tags (co-occurrence) for a given tag | P0 |
| F3.8 | Tag autocomplete | P0 |

### 5.4 Pattern Discovery

| ID | Requirement | Priority |
|----|-------------|----------|
| F4.1 | Compute tag co-occurrence across all moments | P0 |
| F4.2 | Rank patterns by average virality score | P0 |
| F4.3 | Filter patterns by minimum occurrence count | P0 |
| F4.4 | Show example moments for each pattern | P1 |
| F4.5 | Scheduled pattern recomputation | P2 |

### 5.5 User Interface

| ID | Requirement | Priority |
|----|-------------|----------|
| F5.1 | Search page with tag selection and results | P0 |
| F5.2 | Video list page | P0 |
| F5.3 | Tag browser organized by dimension | P0 |
| F5.4 | Pattern discovery page | P0 |
| F5.5 | Upload page for new videos/transcripts | P0 |
| F5.6 | Moment detail view with all metadata | P1 |
| F5.7 | Export moments to CSV | P2 |

---

## 6. Tag Taxonomy

### 6.1 Dimensions

| Dimension | Purpose | Example Tags |
|-----------|---------|--------------|
| **content_type** | What type of content | food-moment, crowd-interaction, milestone-celebration |
| **emotion** | Emotional tone | excited, overwhelmed, vulnerable, grateful |
| **interaction** | Social dynamics | greeting, negotiation, bonding, conflict |
| **physical** | Physical activity/environment | backflip, dance, crowd-rush, rooftop |
| **viral_marker** | Viral potential indicators | quotable-moment, unexpected-twist, meme-potential |
| **archetype** | Known viral patterns | doppelganger-reveal, food-reaction, milestone-hit |

### 6.2 Complete Tag List (MVP)

```
content_type (12 tags):
  cultural-experience, food-moment, physical-activity, crowd-interaction,
  celebrity-encounter, historical-education, milestone-celebration,
  technical-issue, health-incident, gift-exchange, language-learning, transportation

emotion (10 tags):
  excited, overwhelmed, grateful, frustrated, scared,
  confused, proud, embarrassed, vulnerable, playful

interaction (10 tags):
  greeting, negotiation, teaching, challenging, flirting,
  rejection, bonding, conflict, language-barrier, crowd-chanting

physical (10 tags):
  backflip, dance, race, horse-riding, eating,
  crowd-rush, rooftop, market, vehicle, rain

viral_marker (10 tags):
  quotable-moment, visual-spectacle, unexpected-twist, relatable,
  meme-potential, reaction-bait, wholesome, chaotic, cringe, flex

archetype (10 tags):
  doppelganger-reveal, food-reaction, near-miss, milestone-hit,
  genuine-connection, cultural-shock, physical-fail, physical-win,
  crowd-chaos, blessing-received

TOTAL: 62 tags across 6 dimensions
```

---

## 7. Data Model

### 7.1 Entity Relationship

```
┌─────────────┐       ┌──────────────┐       ┌─────────────┐
│   videos    │───────│  transcripts │       │    tags     │
├─────────────┤  1:1  ├──────────────┤       ├─────────────┤
│ id (PK)     │       │ id (PK)      │       │ id (PK)     │
│ title       │       │ video_id(FK) │       │ slug        │
│ creator     │       │ raw_text     │       │ name        │
│ duration    │       │ status       │       │ dimension   │
│ metadata    │       └──────────────┘       │ usage_count │
└─────────────┘                              └─────────────┘
      │                                             │
      │ 1:N                                         │ M:N
      ▼                                             ▼
┌─────────────┐       ┌──────────────────┐
│   moments   │───────│  moment_tags     │
├─────────────┤  1:N  ├──────────────────┤
│ id (PK)     │       │ moment_id (FK)   │
│ video_id    │       │ tag_id (FK)      │
│ start_time  │       │ confidence       │
│ end_time    │       └──────────────────┘
│ summary     │
│ virality_*  │       ┌──────────────────┐
│ platform_*  │       │ tag_correlations │
│ embedding   │       ├──────────────────┤
└─────────────┘       │ tag_pattern[]    │
                      │ occurrence_count │
                      │ avg_virality     │
                      └──────────────────┘
```

### 7.2 Key Fields

**moments table:**
- `virality_hook_strength` (0-10): How strong is the opening hook?
- `virality_shareability` (0-10): How likely to be shared?
- `virality_clip_independence` (0-10): Can it stand alone?
- `virality_emotional_intensity` (0-10): How emotionally impactful?
- `platform_tiktok/shorts/reels/twitter` (0-10): Platform fit scores
- `embedding` (vector[1536]): For semantic similarity search
- `requires_context`: none | title_only | brief | heavy

---

## 8. API Specification

### 8.1 Core Endpoints

```
Videos
  POST   /api/videos                    Create video + transcript
  GET    /api/videos                    List videos (paginated)
  GET    /api/videos/:id                Get video details
  POST   /api/videos/:id/analyze        Trigger AI analysis
  GET    /api/videos/:id/moments        Get video moments
  GET    /api/videos/:id/status         Analysis status

Moments  
  GET    /api/moments/:id               Get moment details
  GET    /api/moments/top               Top viral moments
  DELETE /api/moments/:id               Delete moment
  
Tags
  GET    /api/tags                      List all tags by dimension
  GET    /api/tags/flat                 Flat tag list
  GET    /api/tags/stats                Tag usage statistics
  GET    /api/tags/:slug/moments        Moments for a tag
  
Search
  POST   /api/search/tags               Tag-based search
  POST   /api/search/semantic           Vector similarity search
  POST   /api/search/patterns           Tag correlation patterns
  GET    /api/search/autocomplete       Tag autocomplete
  GET    /api/search/related-tags/:slug Co-occurring tags
  GET    /api/search/full-text          Full-text transcript search
```

### 8.2 Key Request/Response Examples

**Tag Search:**
```json
POST /api/search/tags
{
  "tags": ["food-reaction", "chaotic"],
  "operator": "AND",
  "min_virality": 6.0,
  "limit": 50,
  "offset": 0
}

Response:
{
  "moments": [...],
  "total_count": 127,
  "query_time_ms": 45
}
```

**Pattern Discovery:**
```json
POST /api/search/patterns
{
  "min_occurrences": 5,
  "min_virality": 7.0,
  "limit": 20
}

Response:
{
  "patterns": [
    {
      "tag_pattern": ["crowd-rush", "milestone-hit", "excited"],
      "occurrence_count": 34,
      "avg_virality": 8.9,
      "example_moments": [...]
    }
  ]
}
```

---

## 9. Technical Architecture

### 9.1 Stack

| Layer | Technology | Rationale |
|-------|------------|-----------|
| Frontend | React + Vite + Tailwind | Fast dev, modern tooling |
| Backend | Python FastAPI | Async, fast, great typing |
| Database | PostgreSQL + pgvector | Relational + vector search |
| AI Analysis | Claude API (Sonnet) | Best-in-class reasoning |
| Embeddings | OpenAI text-embedding-3-small | High quality, fast |
| Queue | Redis + Celery (P1) | Background job processing |

### 9.2 Processing Pipeline

```
1. UPLOAD      → Video metadata + transcript text
2. CHUNK       → Split into 3-min segments with 30s overlap
3. ANALYZE     → Claude processes each chunk (parallel, max 5)
4. TAG         → Map slugs to IDs, create moment_tags
5. EMBED       → Generate vector for semantic search
6. INDEX       → Update FTS + vector indices
7. CORRELATE   → Update tag co-occurrence patterns
```

### 9.3 Scale Strategy

| Challenge | Solution |
|-----------|----------|
| Large transcripts | Chunking with overlap |
| API rate limits | Semaphore-controlled concurrency |
| Search latency | GIN + IVFFlat indices |
| Pattern computation | Materialized views / scheduled jobs |
| Many videos | Connection pooling, partitioning |

---

## 10. MVP Scope

### In Scope (MVP)
- ✅ Manual video + transcript upload
- ✅ Claude-powered moment extraction and tagging
- ✅ 62 tags across 6 dimensions
- ✅ Virality and platform scoring
- ✅ Tag-based search with AND/OR
- ✅ Semantic similarity search
- ✅ Pattern discovery
- ✅ React UI for search, browse, upload

### Out of Scope (Future)
- ❌ YouTube transcript auto-fetch
- ❌ Video file upload (processing audio/video)
- ❌ User authentication
- ❌ Team/workspace features
- ❌ Clip export/editing
- ❌ Analytics dashboard
- ❌ Webhook notifications
- ❌ Custom tag creation

---

## 11. File Manifest

```
viral-clip-finder/
├── ARCHITECTURE.md              # System design documentation
├── backend/
│   ├── app/
│   │   ├── main.py              # FastAPI application
│   │   ├── config.py            # Environment settings
│   │   ├── database.py          # DB connection
│   │   ├── models/models.py     # SQLAlchemy ORM
│   │   ├── schemas/schemas.py   # Pydantic schemas
│   │   ├── api/
│   │   │   ├── videos.py        # Video endpoints
│   │   │   ├── moments.py       # Moment endpoints
│   │   │   ├── tags.py          # Tag endpoints
│   │   │   └── search.py        # Search endpoints
│   │   ├── services/
│   │   │   ├── analyzer.py      # AI analysis service
│   │   │   └── embeddings.py    # Vector generation
│   │   └── prompts/
│   │       └── moment_tagger.py # AI prompt templates
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # Main React application
│   │   ├── main.jsx             # Entry point
│   │   └── index.css            # Tailwind styles
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
└── database/
    └── schema.sql               # PostgreSQL schema + seeds
```

---

## 12. Success Criteria for MVP

| Criterion | Measurement |
|-----------|-------------|
| Functional | Can upload transcript, analyze, search by tags |
| Performance | Search returns in < 200ms |
| Quality | AI tags match human judgment 85%+ |
| Scale | Handles 100 videos, 5000 moments without degradation |
| Usability | Non-technical user can upload and search |

---

## 13. Open Questions

1. **Tag expansion:** How do we handle new tag suggestions from AI that aren't in taxonomy?
2. **Confidence thresholds:** Should we filter low-confidence tags from display?
3. **Pattern minimum:** What's the right threshold for surfacing patterns (5? 10? occurrences)?
4. **Embedding cost:** At scale, embedding generation could be expensive—batch strategy?
5. **Multi-language:** How to handle non-English transcripts?

---

## 14. Appendix: Example AI Output

```json
{
  "moments": [
    {
      "start_time": 245.0,
      "end_time": 280.0,
      "summary": "Speed tries raw Ethiopian meat for the first time and has an intense reaction",
      "transcript_excerpt": "What is this?! This is RAW! They eat this RAW?!",
      "tags": {
        "content_type": ["food-moment", "cultural-experience"],
        "emotion": ["scared", "overwhelmed"],
        "interaction": ["teaching"],
        "physical": ["eating"],
        "viral_marker": ["reaction-bait", "quotable-moment"],
        "archetype": ["food-reaction", "cultural-shock"]
      },
      "virality_scores": {
        "hook_strength": 9,
        "shareability": 8,
        "clip_independence": 9,
        "emotional_intensity": 8
      },
      "platform_scores": {
        "tiktok": 9,
        "youtube_shorts": 8,
        "instagram_reels": 7,
        "twitter": 6
      },
      "clip_metadata": {
        "suggested_start": 243.0,
        "suggested_end": 278.0,
        "hook_lines": [
          "Speed tries RAW MEAT in Ethiopia 😱",
          "His reaction to Ethiopian raw beef is INSANE",
          "When you realize they eat it RAW..."
        ],
        "requires_context": "none"
      }
    }
  ]
}
```

---

*Document generated as part of Viral Clip Finder MVP design.*
