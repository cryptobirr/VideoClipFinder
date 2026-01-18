"""FastAPI application entry point"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    # Startup
    print("🚀 Viral Clip Finder API starting...")
    print(f"📊 Database: {settings.database_url}")
    print(f"🤖 Claude Agent SDK: Using Claude Max authentication")

    yield

    # Shutdown
    print("👋 Shutting down...")


app = FastAPI(
    title="Viral Clip Finder API",
    description="AI-powered viral moment detection and tagging system",
    version="0.1.0",
    lifespan=lifespan,
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": "Viral Clip Finder API",
        "version": "0.1.0",
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "agent_sdk": "ready",
    }


# Import and include routers here (after they're created)
# from app.api import videos, moments, tags, search
# app.include_router(videos.router, prefix="/api/videos", tags=["videos"])
# app.include_router(moments.router, prefix="/api/moments", tags=["moments"])
# app.include_router(tags.router, prefix="/api/tags", tags=["tags"])
# app.include_router(search.router, prefix="/api/search", tags=["search"])
