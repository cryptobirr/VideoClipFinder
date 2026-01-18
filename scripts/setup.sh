#!/bin/bash
set -e

echo "🎬 Viral Clip Finder - Setup Script"
echo "======================================"

# Check prerequisites
echo ""
echo "Checking prerequisites..."

# Check Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js not found. Please install Node.js 20+"
    exit 1
fi
echo "✅ Node.js $(node --version)"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python not found. Please install Python 3.12+"
    exit 1
fi
echo "✅ Python $(python3 --version)"

# Check Claude Code CLI
if ! command -v claude &> /dev/null; then
    echo "⚠️  Claude Code CLI not found"
    echo "   Install: npm install -g @anthropic-ai/claude-code"
    echo "   Then run: claude login"
else
    echo "✅ Claude Code CLI installed"
fi

# Check Docker (optional)
if command -v docker &> /dev/null; then
    echo "✅ Docker $(docker --version | cut -d' ' -f3)"
else
    echo "⚠️  Docker not found (optional - for local PostgreSQL)"
fi

# Install pnpm globally
echo ""
echo "Installing pnpm..."
if ! command -v pnpm &> /dev/null; then
    npm install -g pnpm
    echo "✅ pnpm installed"
else
    echo "✅ pnpm already installed"
fi

# Install uv for Python
echo ""
echo "Installing uv (Python package manager)..."
if ! command -v uv &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh
    echo "✅ uv installed"
else
    echo "✅ uv already installed"
fi

# Create .env from example
echo ""
echo "Setting up environment..."
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ Created .env file (please update with your values)"
else
    echo "✅ .env file already exists"
fi

# Backend setup
echo ""
echo "Setting up Python backend..."
cd backend
uv pip install -e .
cd ..
echo "✅ Backend dependencies installed"

# Frontend setup
echo ""
echo "Setting up React frontend..."
cd frontend
pnpm install
cd ..
echo "✅ Frontend dependencies installed"

# Start database
echo ""
echo "Starting PostgreSQL with Docker..."
if command -v docker &> /dev/null; then
    docker-compose up -d postgres
    echo "✅ PostgreSQL started on port 5432"
    echo "   Waiting for database to be ready..."
    sleep 5
else
    echo "⚠️  Docker not available - please set up PostgreSQL manually"
    echo "   See database/README.md for instructions"
fi

# Summary
echo ""
echo "======================================"
echo "✨ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Run 'claude login' if you haven't already"
echo "2. Update .env with your database credentials"
echo "3. Run 'scripts/dev.sh' to start development servers"
echo ""
echo "Useful commands:"
echo "  scripts/dev.sh        - Start all services"
echo "  scripts/test.sh       - Run tests"
echo "  scripts/db-init.sh    - Initialize database"
echo ""
