#!/bin/bash

echo "🚀 Starting Viral Clip Finder development servers..."
echo ""

# Start PostgreSQL in background
echo "Starting PostgreSQL..."
docker-compose up -d postgres

# Wait for database
echo "Waiting for database..."
sleep 3

# Start backend in background
echo "Starting backend (http://localhost:8000)..."
cd backend
uv run uvicorn app.main:app --reload &
BACKEND_PID=$!
cd ..

# Start frontend in background
echo "Starting frontend (http://localhost:5173)..."
cd frontend
pnpm dev &
FRONTEND_PID=$!
cd ..

echo ""
echo "✨ Development servers running:"
echo "   Frontend: http://localhost:5173"
echo "   Backend:  http://localhost:8000"
echo "   API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all servers"
echo ""

# Wait for Ctrl+C
trap "kill $BACKEND_PID $FRONTEND_PID; docker-compose down; exit" INT
wait
