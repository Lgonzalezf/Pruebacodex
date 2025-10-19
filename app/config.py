from __future__ import annotations

from dataclasses import dataclass
import os
from typing import Optional

from dotenv import load_dotenv


@dataclass
class Settings:
    """Application configuration loaded from environment variables."""

    database_url: str
    schema: Optional[str] = None

    @classmethod
    def load(cls) -> "Settings":
        load_dotenv()

        database_url = os.environ.get("DATABASE_URL")
        if not database_url:
            raise RuntimeError(
                "DATABASE_URL is required. Set it in the environment or .env file."
            )

        schema = os.environ.get("DATABASE_SCHEMA")
        return cls(database_url=database_url, schema=schema)


__all__ = ["Settings"]
