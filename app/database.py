from __future__ import annotations

from sqlalchemy import create_engine
from sqlalchemy.engine import Engine


def get_engine(database_url: str) -> Engine:
    """Create a SQLAlchemy engine for the provided database URL."""

    return create_engine(database_url, future=True)


__all__ = ["get_engine"]
