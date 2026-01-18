# Database Setup

## Prerequisites

- PostgreSQL 15+ with pgvector extension
- Supabase account (recommended) or local PostgreSQL instance

## Local Development with Docker

```bash
# Start PostgreSQL with pgvector
docker run -d \
  --name viral-clip-db \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=viral_clip_finder \
  -p 5432:5432 \
  ankane/pgvector
```

## Initialize Database

```bash
# Connect to database
psql postgresql://postgres:postgres@localhost:5432/viral_clip_finder

# Run schema
\i database/schema.sql
```

## Using Supabase (Recommended)

1. Create new project at https://supabase.com
2. Get connection string from Settings → Database
3. Enable pgvector extension:
   - Go to Database → Extensions
   - Search for "vector" and enable it
4. Run schema.sql in SQL Editor

## Connection String Format

```env
# Local
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/viral_clip_finder

# Supabase
DATABASE_URL=postgresql://postgres:[PASSWORD]@[PROJECT].supabase.co:5432/postgres
```

## Migrations (Future)

When schema changes are needed:

```bash
cd backend

# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head
```
