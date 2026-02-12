"""Load cached pin data for the Shiny app.

Reads Parquet files from the pin cache. Falls back to sample/empty DataFrames
when data is not yet available (first run or failed ETL).
"""

import logging
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "pin_cache"


def read_pin(name: str) -> pd.DataFrame:
    """Read a pinned DataFrame from the local cache."""
    data_path = _CACHE_DIR / name / "data.parquet"
    if data_path.exists():
        return pd.read_parquet(data_path)
    logger.warning("Pin '%s' not found at %s — returning empty DataFrame", name, data_path)
    return pd.DataFrame()


def pin_updated_at(name: str) -> str:
    """Return the last-updated timestamp for a pin, or 'Never' if missing."""
    import json
    meta_path = _CACHE_DIR / name / "meta.json"
    if meta_path.exists():
        meta = json.loads(meta_path.read_text())
        return meta.get("updated_at", "Unknown")
    return "Never"


def load_rankings() -> pd.DataFrame:
    return read_pin("rankings")


def load_team_stats() -> pd.DataFrame:
    return read_pin("team_stats")


def load_individual_stats() -> pd.DataFrame:
    return read_pin("individual_stats")


def load_standings() -> pd.DataFrame:
    return read_pin("standings")


def load_schedule() -> pd.DataFrame:
    df = read_pin("schedule")
    if not df.empty and "date" in df.columns:
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
    return df


def load_schools() -> pd.DataFrame:
    return read_pin("schools")


def load_live_scores() -> pd.DataFrame:
    return read_pin("live_scores")


def load_brackets() -> pd.DataFrame:
    return read_pin("brackets")
