import { useState } from 'react';

const tabs = ['Overview', 'Data Model', 'AI Agent', 'API', 'Demo'];

// Simple tag component
function Tag({ children, color = 'purple' }) {
  const colors = {
    purple: 'bg-purple-500/20 text-purple-300 border-purple-500/40',
    blue: 'bg-blue-500/20 text-blue-300 border-blue-500/40',
    green: 'bg-green-500/20 text-green-300 border-green-500/40',
    amber: 'bg-amber-500/20 text-amber-300 border-amber-500/40',
    red: 'bg-red-500/20 text-red-300 border-red-500/40',
  };
  return (
    <span className={`inline-block px-2 py-1 rounded text-xs border ${colors[color]}`}>
      {children}
    </span>
  );
}

function OverviewTab() {
  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-purple-900/40 to-blue-900/40 rounded-xl p-6 border border-purple-500/30">
        <h2 className="text-xl font-bold text-white mb-2">Viral Clip Finder</h2>
        <p className="text-slate-300">
          AI-powered system to analyze video transcripts, tag moments, and discover viral patterns across thousands of videos.
        </p>
      </div>

      <div className="grid grid-cols-3 gap-4">
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="text-2xl mb-2">⚛️</div>
          <h3 className="font-bold text-white">React + Vite</h3>
          <p className="text-sm text-slate-400">Search, explore, upload UI</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="text-2xl mb-2">🐍</div>
          <h3 className="font-bold text-white">FastAPI</h3>
          <p className="text-sm text-slate-400">Async REST backend</p>
        </div>
        <div className="bg-slate-800 rounded-lg p-4 border border-slate-700">
          <div className="text-2xl mb-2">🐘</div>
          <h3 className="font-bold text-white">PostgreSQL + pgvector</h3>
          <p className="text-sm text-slate-400">Scalable storage + vector search</p>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Processing Pipeline</h3>
        <div className="flex flex-wrap gap-2 items-center text-sm">
          {['Upload', '→', 'Chunk', '→', 'Claude AI', '→', 'Tag', '→', 'Embed', '→', 'Index', '→', 'Correlate'].map((step, i) => (
            step === '→' ? 
              <span key={i} className="text-slate-500">→</span> :
              <span key={i} className="bg-purple-500/20 text-purple-300 px-3 py-1 rounded">{step}</span>
          ))}
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Scale Targets</h3>
        <div className="grid grid-cols-4 gap-4 text-center">
          <div>
            <div className="text-2xl font-bold text-purple-400">10K+</div>
            <div className="text-xs text-slate-400">Videos</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-400">1M+</div>
            <div className="text-xs text-slate-400">Moments</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-400">50+</div>
            <div className="text-xs text-slate-400">Tags/Moment</div>
          </div>
          <div>
            <div className="text-2xl font-bold text-purple-400">&lt;100ms</div>
            <div className="text-xs text-slate-400">Search</div>
          </div>
        </div>
      </div>
    </div>
  );
}

function DataModelTab() {
  return (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Core Tables</h3>
        <pre className="text-xs text-slate-300 overflow-x-auto">{`
videos          moments              tags
--------        --------             --------
id (PK)         id (PK)              id (PK)
title           video_id (FK)        slug
creator         start_time           name
duration        end_time             dimension
                summary              usage_count
                virality_* (4)
                platform_* (4)       moment_tags
                embedding            -----------
                                     moment_id (FK)
                                     tag_id (FK)
                                     confidence
        `}</pre>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Tag Dimensions (62 tags total)</h3>
        <div className="space-y-3">
          <div>
            <Tag color="blue">content_type</Tag>
            <p className="text-xs text-slate-400 mt-1">food-moment, crowd-interaction, milestone-celebration, physical-activity...</p>
          </div>
          <div>
            <Tag color="red">emotion</Tag>
            <p className="text-xs text-slate-400 mt-1">excited, overwhelmed, vulnerable, grateful, scared, confused...</p>
          </div>
          <div>
            <Tag color="purple">interaction</Tag>
            <p className="text-xs text-slate-400 mt-1">greeting, negotiation, bonding, conflict, flirting, rejection...</p>
          </div>
          <div>
            <Tag color="green">physical</Tag>
            <p className="text-xs text-slate-400 mt-1">backflip, dance, crowd-rush, rooftop, eating, race...</p>
          </div>
          <div>
            <Tag color="amber">viral_marker</Tag>
            <p className="text-xs text-slate-400 mt-1">quotable-moment, unexpected-twist, meme-potential, wholesome, chaotic...</p>
          </div>
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Key Indices</h3>
        <ul className="text-sm text-slate-300 space-y-2">
          <li>• <code className="text-purple-300">GIN</code> - Full-text search on summaries</li>
          <li>• <code className="text-purple-300">IVFFlat</code> - Vector similarity (pgvector)</li>
          <li>• <code className="text-purple-300">B-tree</code> - Tag and time lookups</li>
        </ul>
      </div>
    </div>
  );
}

function AIAgentTab() {
  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-green-900/40 to-emerald-900/40 rounded-xl p-6 border border-green-500/30">
        <h2 className="text-xl font-bold text-white mb-2">🤖 Claude AI Tagging Agent</h2>
        <p className="text-slate-300">
          Processes 3-minute transcript chunks, extracting moments with multi-dimensional tags and virality scores.
        </p>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Output Per Moment</h3>
        <pre className="text-xs text-green-300 overflow-x-auto">{`{
  "start_time": 245.0,
  "end_time": 280.0,
  "summary": "Speed tries raw Ethiopian meat...",
  "tags": {
    "content_type": ["food-moment"],
    "emotion": ["scared", "overwhelmed"],
    "viral_marker": ["reaction-bait"]
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
}`}</pre>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Processing Steps</h3>
        <ol className="text-sm text-slate-300 space-y-2">
          <li>1. <strong>Chunk</strong> - Split transcript into 3-min segments (30s overlap)</li>
          <li>2. <strong>Analyze</strong> - Claude processes chunks in parallel (max 5)</li>
          <li>3. <strong>Map Tags</strong> - Convert slugs to database IDs</li>
          <li>4. <strong>Embed</strong> - Generate vector for semantic search</li>
          <li>5. <strong>Correlate</strong> - Update tag co-occurrence patterns</li>
        </ol>
      </div>
    </div>
  );
}

function APITab() {
  const endpoints = [
    { method: 'POST', path: '/api/videos', desc: 'Create video + transcript' },
    { method: 'POST', path: '/api/videos/:id/analyze', desc: 'Trigger AI analysis' },
    { method: 'POST', path: '/api/search/tags', desc: 'Search by tag combo' },
    { method: 'POST', path: '/api/search/semantic', desc: 'Vector similarity' },
    { method: 'POST', path: '/api/search/patterns', desc: 'Tag correlations' },
    { method: 'GET', path: '/api/tags', desc: 'List all tags' },
  ];

  return (
    <div className="space-y-6">
      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Core Endpoints</h3>
        <div className="space-y-2">
          {endpoints.map((ep, i) => (
            <div key={i} className="flex items-center gap-3 text-sm">
              <span className={`px-2 py-0.5 rounded text-xs font-bold ${ep.method === 'GET' ? 'bg-green-500/20 text-green-400' : 'bg-blue-500/20 text-blue-400'}`}>
                {ep.method}
              </span>
              <code className="text-purple-300 flex-1">{ep.path}</code>
              <span className="text-slate-400">{ep.desc}</span>
            </div>
          ))}
        </div>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Tag Search Example</h3>
        <pre className="text-xs text-blue-300 overflow-x-auto">{`POST /api/search/tags
{
  "tags": ["food-reaction", "chaotic"],
  "operator": "AND",
  "min_virality": 6.0
}

→ Returns 127 moments across all videos`}</pre>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Pattern Discovery</h3>
        <pre className="text-xs text-amber-300 overflow-x-auto">{`POST /api/search/patterns
{ "min_occurrences": 5, "min_virality": 7.0 }

→ Discovers:
  ["crowd-rush", "milestone-hit"] = 8.9 avg virality
  ["food-reaction", "disgusted"]  = 8.1 avg virality`}</pre>
      </div>
    </div>
  );
}

function DemoTab() {
  const [selected, setSelected] = useState([]);
  const [results, setResults] = useState(null);

  const tags = ['food-reaction', 'crowd-rush', 'milestone-hit', 'doppelganger-reveal', 'chaotic', 'wholesome'];
  
  const mockData = {
    'food-reaction': [
      { time: '4:01:45', summary: 'Speed tries raw Ethiopian meat', virality: 8.2 },
      { time: '0:36:52', summary: 'Tasting Ethiopian coffee ceremony', virality: 7.8 },
    ],
    'crowd-rush': [
      { time: '3:38:15', summary: 'Massive crowd surrounds the car', virality: 9.1 },
    ],
    'milestone-hit': [
      { time: '1:56:00', summary: 'Hits 48.5M subscribers live', virality: 9.5 },
    ],
    'doppelganger-reveal': [
      { time: '1:48:50', summary: 'Speed meets his Ethiopian lookalike', virality: 9.3 },
    ],
  };

  const toggle = (tag) => {
    if (selected.includes(tag)) {
      setSelected(selected.filter(t => t !== tag));
    } else {
      setSelected([...selected, tag]);
    }
  };

  const search = () => {
    const found = selected.flatMap(t => mockData[t] || []);
    setResults(found.sort((a, b) => b.virality - a.virality));
  };

  return (
    <div className="space-y-6">
      <div className="bg-gradient-to-r from-blue-900/40 to-cyan-900/40 rounded-xl p-6 border border-blue-500/30">
        <h2 className="text-xl font-bold text-white mb-2">🔍 Try Tag Search</h2>
        <p className="text-slate-300">Select tags to find matching moments (sample data from IShowSpeed Ethiopia stream)</p>
      </div>

      <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
        <h3 className="font-bold text-white mb-3">Select Tags</h3>
        <div className="flex flex-wrap gap-2 mb-4">
          {tags.map(tag => (
            <button
              key={tag}
              onClick={() => toggle(tag)}
              className={`px-3 py-1.5 rounded text-sm transition-all ${
                selected.includes(tag) 
                  ? 'bg-purple-500 text-white' 
                  : 'bg-slate-700 text-slate-300 hover:bg-slate-600'
              }`}
            >
              {tag}
            </button>
          ))}
        </div>
        <button
          onClick={search}
          disabled={selected.length === 0}
          className="bg-purple-500 hover:bg-purple-600 disabled:opacity-50 text-white px-4 py-2 rounded"
        >
          Search Moments
        </button>
      </div>

      {results && (
        <div className="bg-slate-800/50 rounded-lg p-4 border border-slate-700">
          <h3 className="font-bold text-white mb-3">Found {results.length} Moments</h3>
          <div className="space-y-3">
            {results.map((r, i) => (
              <div key={i} className="flex items-center gap-4 bg-slate-900 rounded p-3">
                <div className="text-slate-400 text-sm w-16">{r.time}</div>
                <div className="flex-1 text-white">{r.summary}</div>
                <div className={`text-lg font-bold ${r.virality >= 9 ? 'text-purple-400' : r.virality >= 8 ? 'text-green-400' : 'text-amber-400'}`}>
                  {r.virality}
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default function App() {
  const [activeTab, setActiveTab] = useState('Overview');

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6">
      <div className="max-w-4xl mx-auto">
        <div className="flex items-center gap-4 mb-6">
          <div className="w-12 h-12 rounded-xl bg-gradient-to-br from-purple-500 to-pink-500 flex items-center justify-center text-2xl">
            ⚡
          </div>
          <div>
            <h1 className="text-2xl font-bold text-white">Viral Clip Finder</h1>
            <p className="text-slate-400 text-sm">AI Video Moment Tagging System</p>
          </div>
        </div>

        <div className="flex gap-1 mb-6 border-b border-slate-700">
          {tabs.map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 text-sm font-medium transition-all ${
                activeTab === tab
                  ? 'text-purple-400 border-b-2 border-purple-400'
                  : 'text-slate-400 hover:text-white'
              }`}
            >
              {tab}
            </button>
          ))}
        </div>

        {activeTab === 'Overview' && <OverviewTab />}
        {activeTab === 'Data Model' && <DataModelTab />}
        {activeTab === 'AI Agent' && <AIAgentTab />}
        {activeTab === 'API' && <APITab />}
        {activeTab === 'Demo' && <DemoTab />}

        <div className="mt-8 pt-4 border-t border-slate-800 text-center text-sm text-slate-500">
          Complete MVP codebase in /home/claude/viral-clip-finder/
        </div>
      </div>
    </div>
  );
}
