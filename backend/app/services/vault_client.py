"""HashiCorp Vault client for secrets management"""
import os
from typing import Any

import httpx

from app.config import settings


class VaultClient:
    """Client for HashiCorp Vault integration"""

    def __init__(self):
        self.vault_addr = settings.vault_addr
        self.vault_token = settings.vault_token or os.getenv("VAULT_TOKEN")
        self.enabled = settings.vault_enabled and self.vault_token is not None

        if self.enabled:
            self.client = httpx.Client(
                base_url=self.vault_addr,
                headers={"X-Vault-Token": self.vault_token},
                timeout=10.0,
            )
        else:
            self.client = None

    def get_secret(self, path: str) -> dict[str, Any] | None:
        """
        Get secret from Vault

        Args:
            path: Secret path (e.g., "secret/postgres/viral_clip_finder")

        Returns:
            Secret data dict or None if not enabled/found
        """
        if not self.enabled or not self.client:
            return None

        try:
            response = self.client.get(f"/v1/{path}")
            response.raise_for_status()
            data = response.json()
            return data.get("data", {}).get("data", {})
        except Exception as e:
            print(f"Vault error: {e}")
            return None

    def get_database_credentials(self, db_name: str = "viral_clip_finder") -> dict[str, str]:
        """
        Get database credentials from Vault

        Args:
            db_name: Database name

        Returns:
            Dict with host, port, database, username, password
        """
        secret = self.get_secret(f"secret/postgres/{db_name}")
        if secret:
            return {
                "host": secret.get("host", "localhost"),
                "port": secret.get("port", "5432"),
                "database": secret.get("database", db_name),
                "username": secret.get("username", "postgres"),
                "password": secret.get("password", ""),
            }

        # Fallback to environment variables
        return {
            "host": os.getenv("DB_HOST", "localhost"),
            "port": os.getenv("DB_PORT", "5432"),
            "database": os.getenv("DB_NAME", db_name),
            "username": os.getenv("DB_USER", "postgres"),
            "password": os.getenv("DB_PASSWORD", ""),
        }

    def close(self):
        """Close Vault client"""
        if self.client:
            self.client.close()


# Global instance
vault = VaultClient()
