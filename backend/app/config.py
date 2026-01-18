"""Application configuration using Pydantic settings"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

    # Database
    database_url: str = "postgresql://localhost/viral_clip_finder"

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_reload: bool = True

    # CORS
    cors_origins: list[str] = ["http://localhost:5173"]

    # Claude Agent SDK (uses Claude Max authentication via `claude login`)
    # No API key needed - SDK automatically uses your Max subscription

    # Vault (optional - for production secrets)
    vault_addr: str = "http://127.0.0.1:8200"
    vault_token: str | None = None
    vault_enabled: bool = False

    # Processing
    max_concurrent_chunks: int = 5
    transcript_chunk_size: int = 180  # seconds (~3 minutes)
    transcript_chunk_overlap: int = 30  # seconds


settings = Settings()
