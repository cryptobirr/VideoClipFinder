-- Viral Clip Finder - Database Schema
-- PostgreSQL with pgvector extension

-- Enable extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "vector";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- ============================================
-- CORE TABLES
-- ============================================

-- Videos table
CREATE TABLE videos (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    title VARCHAR(500) NOT NULL,
    source_url VARCHAR(2000),
    source_platform VARCHAR(50), -- youtube, twitch, tiktok, etc.
    creator VARCHAR(200),
    creator_id VARCHAR(200),
    duration_seconds INTEGER,
    published_at TIMESTAMP WITH TIME ZONE,
    thumbnail_url VARCHAR(2000),
    
    -- Aggregated stats (updated after analysis)
    moment_count INTEGER DEFAULT 0,
    avg_virality_score FLOAT DEFAULT 0,
    top_tags JSONB DEFAULT '[]'::jsonb,
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Transcripts table
CREATE TABLE transcripts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    
    raw_text TEXT NOT NULL,
    word_count INTEGER,
    language VARCHAR(10) DEFAULT 'en',
    
    -- Processing status
    status VARCHAR(20) DEFAULT 'pending', -- pending, processing, completed, failed
    processed_at TIMESTAMP WITH TIME ZONE,
    error_message TEXT,
    
    -- Source info
    source VARCHAR(50), -- manual, youtube_api, whisper, etc.
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(video_id)
);

-- Tag dimensions (categories of tags)
CREATE TABLE tag_dimensions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    color VARCHAR(7), -- hex color for UI
    icon VARCHAR(50), -- icon name for UI
    sort_order INTEGER DEFAULT 0
);

-- Tags table (hierarchical)
CREATE TABLE tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    dimension_id UUID REFERENCES tag_dimensions(id),
    parent_id UUID REFERENCES tags(id),
    
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    description TEXT,
    
    -- For UI display
    color VARCHAR(7),
    icon VARCHAR(50),
    
    -- Usage stats
    usage_count INTEGER DEFAULT 0,
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(dimension_id, name)
);

-- Moments table (the core entity)
CREATE TABLE moments (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    
    -- Timing
    start_time FLOAT NOT NULL, -- seconds
    end_time FLOAT NOT NULL,   -- seconds
    duration_seconds FLOAT GENERATED ALWAYS AS (end_time - start_time) STORED,
    
    -- Content
    summary TEXT NOT NULL,
    transcript_excerpt TEXT,
    
    -- Virality scores (0-10)
    virality_hook_strength FLOAT DEFAULT 0,
    virality_shareability FLOAT DEFAULT 0,
    virality_clip_independence FLOAT DEFAULT 0,
    virality_emotional_intensity FLOAT DEFAULT 0,
    virality_overall FLOAT GENERATED ALWAYS AS (
        (virality_hook_strength + virality_shareability + virality_clip_independence + virality_emotional_intensity) / 4
    ) STORED,
    
    -- Platform fit scores (0-10)
    platform_tiktok FLOAT DEFAULT 0,
    platform_youtube_shorts FLOAT DEFAULT 0,
    platform_instagram_reels FLOAT DEFAULT 0,
    platform_twitter FLOAT DEFAULT 0,
    
    -- Clip metadata
    suggested_clip_start FLOAT,
    suggested_clip_end FLOAT,
    suggested_hook_lines JSONB DEFAULT '[]'::jsonb,
    requires_context VARCHAR(20) DEFAULT 'none', -- none, title_only, brief, heavy
    
    -- Embedding for semantic search (1536 dimensions for OpenAI, adjust as needed)
    embedding vector(1536),
    
    -- Extended metadata
    metadata JSONB DEFAULT '{}'::jsonb,
    
    -- Processing
    analyzed_at TIMESTAMP WITH TIME ZONE,
    analysis_version VARCHAR(20),
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Moment-Tag junction table
CREATE TABLE moment_tags (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    moment_id UUID NOT NULL REFERENCES moments(id) ON DELETE CASCADE,
    tag_id UUID NOT NULL REFERENCES tags(id) ON DELETE CASCADE,
    
    -- Confidence and context
    confidence FLOAT DEFAULT 1.0, -- 0-1, how confident the AI is
    context TEXT, -- why this tag was applied
    
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    UNIQUE(moment_id, tag_id)
);

-- ============================================
-- ANALYTICS & CORRELATION TABLES
-- ============================================

-- Tag co-occurrence patterns
CREATE TABLE tag_correlations (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    
    -- The tag pattern (array of tag IDs)
    tag_pattern UUID[] NOT NULL,
    tag_pattern_slugs VARCHAR(100)[] NOT NULL, -- for easier querying
    
    -- Stats
    occurrence_count INTEGER DEFAULT 0,
    avg_virality_score FLOAT DEFAULT 0,
    
    -- Sample moments
    example_moment_ids UUID[] DEFAULT '{}',
    
    -- Pattern metadata
    pattern_hash VARCHAR(64) UNIQUE, -- for deduplication
    
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Search history (for analytics)
CREATE TABLE search_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    query_type VARCHAR(50), -- tags, semantic, pattern
    query_params JSONB,
    result_count INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- ============================================
-- INDEXES
-- ============================================

-- Videos
CREATE INDEX idx_videos_creator ON videos(creator);
CREATE INDEX idx_videos_platform ON videos(source_platform);
CREATE INDEX idx_videos_created ON videos(created_at DESC);

-- Transcripts
CREATE INDEX idx_transcripts_video ON transcripts(video_id);
CREATE INDEX idx_transcripts_status ON transcripts(status);

-- Tags
CREATE INDEX idx_tags_dimension ON tags(dimension_id);
CREATE INDEX idx_tags_slug ON tags(slug);
CREATE INDEX idx_tags_usage ON tags(usage_count DESC);

-- Moments
CREATE INDEX idx_moments_video ON moments(video_id);
CREATE INDEX idx_moments_video_time ON moments(video_id, start_time);
CREATE INDEX idx_moments_virality ON moments(virality_overall DESC);
CREATE INDEX idx_moments_analyzed ON moments(analyzed_at);

-- Full-text search on moments
CREATE INDEX idx_moments_fts ON moments 
    USING GIN(to_tsvector('english', COALESCE(summary, '') || ' ' || COALESCE(transcript_excerpt, '')));

-- Vector similarity search
CREATE INDEX idx_moments_embedding ON moments 
    USING ivfflat (embedding vector_cosine_ops) WITH (lists = 100);

-- Moment tags
CREATE INDEX idx_moment_tags_moment ON moment_tags(moment_id);
CREATE INDEX idx_moment_tags_tag ON moment_tags(tag_id);

-- Tag correlations
CREATE INDEX idx_correlations_pattern ON tag_correlations USING GIN(tag_pattern);
CREATE INDEX idx_correlations_virality ON tag_correlations(avg_virality_score DESC);

-- ============================================
-- SEED DATA: TAG DIMENSIONS & TAGS
-- ============================================

-- Insert tag dimensions
INSERT INTO tag_dimensions (name, description, color, icon, sort_order) VALUES
('content_type', 'What type of content is this moment', '#3B82F6', 'film', 1),
('emotion', 'Emotional tone and intensity', '#EF4444', 'heart', 2),
('interaction', 'Social dynamics and interactions', '#8B5CF6', 'users', 3),
('physical', 'Physical activities and environment', '#10B981', 'activity', 4),
('viral_marker', 'Indicators of viral potential', '#F59E0B', 'trending-up', 5),
('platform', 'Platform-specific attributes', '#EC4899', 'share', 6),
('archetype', 'Known viral clip patterns', '#6366F1', 'zap', 7);

-- Insert core tags (content_type dimension)
INSERT INTO tags (dimension_id, name, slug, description) 
SELECT d.id, t.name, t.slug, t.description
FROM tag_dimensions d
CROSS JOIN (VALUES
    ('cultural_experience', 'cultural-experience', 'Learning about or participating in local culture'),
    ('food_moment', 'food-moment', 'Eating, tasting, or reacting to food'),
    ('physical_activity', 'physical-activity', 'Sports, stunts, dancing, or physical challenges'),
    ('crowd_interaction', 'crowd-interaction', 'Engaging with fans or public crowds'),
    ('celebrity_encounter', 'celebrity-encounter', 'Meeting or interacting with famous people'),
    ('historical_education', 'historical-education', 'Learning about history or visiting historical sites'),
    ('milestone_celebration', 'milestone-celebration', 'Celebrating subscriber counts, achievements'),
    ('technical_issue', 'technical-issue', 'Stream problems, lag, equipment failures'),
    ('health_incident', 'health-incident', 'Feeling sick, tired, or having health issues'),
    ('gift_exchange', 'gift-exchange', 'Receiving or giving gifts'),
    ('language_learning', 'language-learning', 'Learning local words or phrases'),
    ('transportation', 'transportation', 'Traveling by vehicle, horse, etc.')
) AS t(name, slug, description)
WHERE d.name = 'content_type';

-- Insert emotion tags
INSERT INTO tags (dimension_id, name, slug, description)
SELECT d.id, t.name, t.slug, t.description
FROM tag_dimensions d
CROSS JOIN (VALUES
    ('excited', 'excited', 'High energy, enthusiasm'),
    ('overwhelmed', 'overwhelmed', 'Too much stimulation, chaos'),
    ('grateful', 'grateful', 'Thankful, appreciative'),
    ('frustrated', 'frustrated', 'Annoyed, impatient'),
    ('scared', 'scared', 'Fear, anxiety'),
    ('confused', 'confused', 'Uncertainty, disorientation'),
    ('proud', 'proud', 'Achievement, accomplishment'),
    ('embarrassed', 'embarrassed', 'Shame, awkwardness'),
    ('vulnerable', 'vulnerable', 'Open, authentic, raw'),
    ('playful', 'playful', 'Joking, having fun')
) AS t(name, slug, description)
WHERE d.name = 'emotion';

-- Insert interaction tags
INSERT INTO tags (dimension_id, name, slug, description)
SELECT d.id, t.name, t.slug, t.description
FROM tag_dimensions d
CROSS JOIN (VALUES
    ('greeting', 'greeting', 'Meeting someone new'),
    ('negotiation', 'negotiation', 'Bargaining, making deals'),
    ('teaching', 'teaching', 'Being taught something'),
    ('challenging', 'challenging', 'Competition or challenge'),
    ('flirting', 'flirting', 'Romantic interest'),
    ('rejection', 'rejection', 'Being turned down'),
    ('bonding', 'bonding', 'Making genuine connection'),
    ('conflict', 'conflict', 'Disagreement or tension'),
    ('language_barrier', 'language-barrier', 'Communication difficulty'),
    ('crowd_chanting', 'crowd-chanting', 'Group vocal participation')
) AS t(name, slug, description)
WHERE d.name = 'interaction';

-- Insert physical tags
INSERT INTO tags (dimension_id, name, slug, description)
SELECT d.id, t.name, t.slug, t.description
FROM tag_dimensions d
CROSS JOIN (VALUES
    ('backflip', 'backflip', 'Backflip stunt'),
    ('dance', 'dance', 'Dancing'),
    ('race', 'race', 'Racing or running'),
    ('horse_riding', 'horse-riding', 'Riding horses'),
    ('eating', 'eating', 'Consuming food'),
    ('crowd_rush', 'crowd-rush', 'Mob movement, crowd surge'),
    ('rooftop', 'rooftop', 'On top of a building'),
    ('market', 'market', 'In a marketplace'),
    ('vehicle', 'vehicle', 'In a car or vehicle'),
    ('rain', 'rain', 'Raining or wet conditions')
) AS t(name, slug, description)
WHERE d.name = 'physical';

-- Insert viral marker tags
INSERT INTO tags (dimension_id, name, slug, description)
SELECT d.id, t.name, t.slug, t.description
FROM tag_dimensions d
CROSS JOIN (VALUES
    ('quotable_moment', 'quotable-moment', 'Memorable phrase or line'),
    ('visual_spectacle', 'visual-spectacle', 'Impressive visual'),
    ('unexpected_twist', 'unexpected-twist', 'Surprise element'),
    ('relatable', 'relatable', 'Universal experience'),
    ('meme_potential', 'meme-potential', 'Could become a meme'),
    ('reaction_bait', 'reaction-bait', 'Provokes strong reactions'),
    ('wholesome', 'wholesome', 'Heartwarming content'),
    ('chaotic', 'chaotic', 'Uncontrolled, wild energy'),
    ('cringe', 'cringe', 'Uncomfortable but watchable'),
    ('flex', 'flex', 'Showing off success')
) AS t(name, slug, description)
WHERE d.name = 'viral_marker';

-- Insert archetype tags
INSERT INTO tags (dimension_id, name, slug, description)
SELECT d.id, t.name, t.slug, t.description
FROM tag_dimensions d
CROSS JOIN (VALUES
    ('doppelganger_reveal', 'doppelganger-reveal', 'Finding a look-alike'),
    ('food_reaction', 'food-reaction', 'Strong reaction to tasting food'),
    ('near_miss', 'near-miss', 'Almost got hurt or failed'),
    ('milestone_hit', 'milestone-hit', 'Reaching subscriber/viewer goal'),
    ('genuine_connection', 'genuine-connection', 'Real emotional moment with stranger'),
    ('cultural_shock', 'cultural-shock', 'Surprised by local custom'),
    ('physical_fail', 'physical-fail', 'Failed stunt or physical mishap'),
    ('physical_win', 'physical-win', 'Successful impressive stunt'),
    ('crowd_chaos', 'crowd-chaos', 'Overwhelming crowd situation'),
    ('blessing_received', 'blessing-received', 'Religious or traditional blessing')
) AS t(name, slug, description)
WHERE d.name = 'archetype';

-- ============================================
-- FUNCTIONS
-- ============================================

-- Function to update video stats after moment changes
CREATE OR REPLACE FUNCTION update_video_stats()
RETURNS TRIGGER AS $$
BEGIN
    UPDATE videos 
    SET 
        moment_count = (SELECT COUNT(*) FROM moments WHERE video_id = COALESCE(NEW.video_id, OLD.video_id)),
        avg_virality_score = (SELECT AVG(virality_overall) FROM moments WHERE video_id = COALESCE(NEW.video_id, OLD.video_id)),
        updated_at = NOW()
    WHERE id = COALESCE(NEW.video_id, OLD.video_id);
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_video_stats
AFTER INSERT OR UPDATE OR DELETE ON moments
FOR EACH ROW EXECUTE FUNCTION update_video_stats();

-- Function to update tag usage count
CREATE OR REPLACE FUNCTION update_tag_usage()
RETURNS TRIGGER AS $$
BEGIN
    IF TG_OP = 'INSERT' THEN
        UPDATE tags SET usage_count = usage_count + 1 WHERE id = NEW.tag_id;
    ELSIF TG_OP = 'DELETE' THEN
        UPDATE tags SET usage_count = usage_count - 1 WHERE id = OLD.tag_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_update_tag_usage
AFTER INSERT OR DELETE ON moment_tags
FOR EACH ROW EXECUTE FUNCTION update_tag_usage();

-- ============================================
-- VIEWS
-- ============================================

-- Moments with their tags (denormalized for easy querying)
CREATE VIEW moments_with_tags AS
SELECT 
    m.*,
    v.title as video_title,
    v.creator as video_creator,
    COALESCE(
        jsonb_agg(
            jsonb_build_object(
                'tag_id', t.id,
                'tag_slug', t.slug,
                'tag_name', t.name,
                'dimension', td.name,
                'confidence', mt.confidence
            )
        ) FILTER (WHERE t.id IS NOT NULL),
        '[]'::jsonb
    ) as tags
FROM moments m
JOIN videos v ON m.video_id = v.id
LEFT JOIN moment_tags mt ON m.id = mt.moment_id
LEFT JOIN tags t ON mt.tag_id = t.id
LEFT JOIN tag_dimensions td ON t.dimension_id = td.id
GROUP BY m.id, v.title, v.creator;

-- Tag statistics
CREATE VIEW tag_stats AS
SELECT 
    t.id,
    t.slug,
    t.name,
    td.name as dimension,
    t.usage_count,
    AVG(m.virality_overall) as avg_virality,
    COUNT(DISTINCT m.video_id) as video_count
FROM tags t
JOIN tag_dimensions td ON t.dimension_id = td.id
LEFT JOIN moment_tags mt ON t.id = mt.tag_id
LEFT JOIN moments m ON mt.moment_id = m.id
GROUP BY t.id, t.slug, t.name, td.name, t.usage_count;
