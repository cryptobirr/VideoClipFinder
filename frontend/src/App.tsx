import { useState } from 'react'

function App() {
  const [count, setCount] = useState(0)

  return (
    <div className="min-h-screen bg-gray-900 text-white">
      <div className="container mx-auto px-4 py-16">
        <div className="max-w-3xl mx-auto text-center">
          <h1 className="text-5xl font-bold mb-6 bg-gradient-to-r from-blue-400 to-purple-600 bg-clip-text text-transparent">
            Viral Clip Finder
          </h1>
          <p className="text-xl text-gray-400 mb-8">
            AI-powered viral moment detection and tagging system
          </p>

          <div className="bg-gray-800 rounded-lg p-8 shadow-xl">
            <h2 className="text-2xl font-semibold mb-4">Coming Soon</h2>
            <p className="text-gray-400 mb-6">
              Transform hours of video content into a searchable database of viral-ready clips
            </p>

            <div className="flex gap-4 justify-center">
              <div className="bg-gray-700 px-6 py-3 rounded-lg">
                <div className="text-2xl font-bold text-blue-400">{count}</div>
                <div className="text-sm text-gray-400">Test Counter</div>
              </div>
              <button
                type="button"
                onClick={() => setCount((count) => count + 1)}
                className="bg-blue-600 hover:bg-blue-700 px-6 py-3 rounded-lg font-semibold transition"
              >
                Increment
              </button>
            </div>
          </div>

          <div className="mt-12 grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-3xl mb-2">🎬</div>
              <h3 className="font-semibold mb-2">AI Tagging</h3>
              <p className="text-sm text-gray-400">
                Claude-powered moment detection with 62-tag taxonomy
              </p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-3xl mb-2">🔍</div>
              <h3 className="font-semibold mb-2">Smart Search</h3>
              <p className="text-sm text-gray-400">
                Tag combinations, semantic search, and pattern discovery
              </p>
            </div>
            <div className="bg-gray-800 p-6 rounded-lg">
              <div className="text-3xl mb-2">📊</div>
              <h3 className="font-semibold mb-2">Virality Scores</h3>
              <p className="text-sm text-gray-400">
                Platform-specific scores for TikTok, YouTube Shorts, and more
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default App
