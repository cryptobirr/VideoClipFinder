# Viral Clip Finder

AI-powered viral moment detection and tagging system that analyzes video transcripts to identify, tag, and score clip-worthy segments.

## Overview

Viral Clip Finder uses Claude Agent SDK to analyze long-form video content (livestreams, podcasts, interviews) and automatically detect viral moments with:
- **62-tag taxonomy** across 6 dimensions (content type, emotion, interaction, physical, viral markers, archetypes)
- **Virality scores** (hook strength, shareability, independence, emotional intensity)
- **Platform-specific fit** (TikTok, YouTube Shorts, Instagram Reels, Twitter)
- **Semantic search** with pgvector for finding similar moments
- **Pattern discovery** to identify what tag combinations correlate with viral success

## Tech Stack

### Backend
- **Python 3.12+** with FastAPI
- **Claude Agent SDK** (uses Claude Max authentication)
- **PostgreSQL** with pgvector extension
- **SQLAlchemy 2.0** for ORM
- **uv** for package management
- **ruff** for linting/formatting

### Frontend
- **React 18** with Vite
- **TypeScript** for type safety
- **Tailwind CSS** + **shadcn/ui** for styling
- **TanStack Query** for API state management
- **Zustand** for client state
- **pnpm** for package management
- **Biome** for linting/formatting

### Infrastructure
- **Supabase** (managed PostgreSQL + pgvector)
- **Docker Compose** for local development
- **HashiCorp Vault** for secrets management

## Prerequisites

- **Node.js 20+** and **pnpm**
- **Python 3.12+** and **uv**
- **Claude Code CLI** (`npm install -g @anthropic-ai/claude-code`)
- **Docker** (for local PostgreSQL)
- **PostgreSQL 15+** with pgvector (or Supabase account)

## Quick Start

### 1. Clone and Install

```bash
git clone https://github.com/cryptobirr/VideoClipFinder.git
cd VideoClipFinder

# Run automated setup
./scripts/setup.sh
```

### 2. Authenticate with Claude

```bash
# Login to Claude Code (uses your Claude Max subscription)
claude login
```

### 3. Configure Environment

```bash
# Copy environment template
cp .env.example .env

# Edit .env with your database credentials
# For local: DATABASE_URL=postgresql://postgres:postgres@localhost:5432/viral_clip_finder
# For Supabase: Use connection string from Supabase dashboard
```

### 4. Start Development Servers

```bash
# Start all services (PostgreSQL, backend, frontend)
./scripts/dev.sh
```

Access:
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## Project Structure

```
VideoClipFinder/
├── .claude/
│   └── agents/
│       └── moment-tagger.md      # Claude agent for viral moment detection
├── backend/
│   ├── app/
│   │   ├── api/                  # API route handlers
│   │   ├── models/               # SQLAlchemy models
│   │   ├── schemas/              # Pydantic schemas
│   │   ├── services/             # Business logic
│   │   │   ├── analyzer.py       # Transcript analysis with Claude
│   │   │   └── vault_client.py   # Vault integration
│   │   ├── config.py             # Settings
│   │   ├── database.py           # DB connection
│   │   └── main.py               # FastAPI app
│   ├── tests/                    # Backend tests
│   └── pyproject.toml            # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── components/           # React components
│   │   ├── pages/                # Page components
│   │   ├── lib/                  # Utilities
│   │   ├── App.tsx               # Main app
│   │   └── main.tsx              # Entry point
│   ├── package.json              # Node dependencies
│   └── vite.config.ts            # Vite configuration
├── database/
│   ├── schema.sql                # PostgreSQL schema with pgvector
│   └── README.md                 # Database setup guide
├── dev/
│   ├── testing/                  # Test files
│   ├── issues/                   # Issue artifacts
│   ├── specs/                    # Specifications
│   └── temp/                     # Temporary files
├── scripts/
│   ├── setup.sh                  # Automated setup
│   └── dev.sh                    # Start dev servers
├── docker-compose.yml            # Local development stack
└── README.md                     # This file
```

## How It Works

### 1. Upload Video + Transcript
```python
# User uploads video metadata and transcript
POST /api/videos
{
  "title": "IShowSpeed Ethiopia Stream",
  "creator": "IShowSpeed",
  "transcript": "...",
  "duration_seconds": 14400
}
```

### 2. AI Analysis with Claude Agent
```python
# Backend chunks transcript and processes with moment-tagger agent
from claude_agent_sdk import query

async for message in query(
    prompt=f"Use the moment-tagger agent to analyze: {chunk}"
):
    # Agent returns tagged moments with scores
```

### 3. Store Tagged Moments
```json
{
  "start_time": 245.0,
  "end_time": 280.0,
  "summary": "Speed tries raw Ethiopian meat",
  "tags": {
    "content_type": ["food-moment", "cultural-experience"],
    "emotion": ["scared", "overwhelmed"],
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
    "youtube_shorts": 8
  }
}
```

### 4. Search & Discover
- **Tag search**: Find all "food-reaction" + "chaotic" moments
- **Semantic search**: "find moments like 'streamer tries weird food'"
- **Pattern discovery**: What tag combos have highest virality?

## Claude Agent SDK Integration

This project uses **Claude Agent SDK** with **filesystem-based agents** instead of direct API calls.

### Agent Definition (`.claude/agents/moment-tagger.md`)

```markdown
---
name: moment-tagger
description: Analyzes video transcripts to identify viral moments
tools: []
model: sonnet
---

You are an expert viral moment detection specialist...
[Full prompt with 62-tag taxonomy, scoring guidelines, output format]
```

### Using the Agent

```python
from claude_agent_sdk import query

async for message in query(
    prompt="Use the moment-tagger agent to analyze this transcript..."
):
    # Process results
```

### Authentication

- Uses **Claude Max authentication** (no API key needed)
- Run `claude login` once to authenticate
- SDK automatically uses your Claude Code Max subscription

## Development

### Backend Development

```bash
cd backend

# Install dependencies
uv pip install -e .

# Run server with hot reload
uv run uvicorn app.main:app --reload

# Run tests
uv run pytest

# Lint and format
uv run ruff check .
uv run ruff format .
```

### Frontend Development

```bash
cd frontend

# Install dependencies
pnpm install

# Run dev server
pnpm dev

# Build for production
pnpm build

# Lint and format
pnpm lint
pnpm format
```

### Database Management

```bash
# Start PostgreSQL with Docker
docker-compose up -d postgres

# Initialize schema
psql postgresql://postgres:postgres@localhost:5432/viral_clip_finder -f database/schema.sql

# Or use Supabase (recommended for production)
# See database/README.md for setup
```

## Architecture

See [viral-clip-finder-ARCHITECTURE.md](viral-clip-finder-ARCHITECTURE.md) for detailed system architecture.

See [viral-clip-finder-PRD.md](viral-clip-finder-PRD.md) for complete product requirements.

## Key Features

### Tag Taxonomy (62 tags across 6 dimensions)

- **content_type**: food-moment, crowd-interaction, milestone-celebration, etc.
- **emotion**: excited, overwhelmed, vulnerable, playful, etc.
- **interaction**: greeting, teaching, bonding, conflict, etc.
- **physical**: backflip, dance, eating, crowd-rush, etc.
- **viral_marker**: quotable-moment, unexpected-twist, meme-potential, etc.
- **archetype**: food-reaction, doppelganger-reveal, milestone-hit, etc.

### Virality Scoring (0-10 scale)

- **hook_strength**: How compelling is the opening?
- **shareability**: How likely to be shared?
- **clip_independence**: Can it stand alone?
- **emotional_intensity**: How impactful?

### Platform Fit Scoring (0-10 scale)

- **TikTok**: Fast-paced, trendy, under 60s
- **YouTube Shorts**: Educational, under 90s
- **Instagram Reels**: Aesthetic, relatable, under 90s
- **Twitter**: Controversial/quotable, under 30s

## API Endpoints

### Videos
- `POST /api/videos` - Create video + transcript
- `GET /api/videos` - List videos
- `GET /api/videos/:id` - Get video details
- `POST /api/videos/:id/analyze` - Trigger AI analysis
- `GET /api/videos/:id/moments` - Get video moments

### Search
- `POST /api/search/tags` - Tag-based search
- `POST /api/search/semantic` - Vector similarity search
- `POST /api/search/patterns` - Tag correlation patterns

### Tags
- `GET /api/tags` - List all tags by dimension
- `GET /api/tags/:slug/moments` - Moments for a tag
- `GET /api/tags/stats` - Tag usage statistics

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

MIT

## Acknowledgments

- Built with [Claude Agent SDK](https://github.com/anthropics/claude-agent-sdk)
- Powered by [Claude AI](https://claude.ai)
- Database: [pgvector](https://github.com/pgvector/pgvector)

---

**Repository**: https://github.com/cryptobirr/VideoClipFinder

For questions or issues, please open a GitHub issue.
