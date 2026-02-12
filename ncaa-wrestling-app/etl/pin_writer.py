"""Write processed DataFrames to a local pin-compatible cache (Parquet files).

On Posit Connect this would use the `pins` library with a Connect board.
For local development and environments without Connect, we use a simple
Parquet-based file cache that mirrors the pins interface.
"""

import json
import logging
import os
from datetime import datetime
from pathlib import Path

import pandas as pd

logger = logging.getLogger(__name__)

_DEFAULT_CACHE_DIR = Path(__file__).resolve().parent.parent / "pin_cache"


class PinWriter:
    """Write and version datasets as Parquet files in a local cache directory."""

    def __init__(self, cache_dir: str | Path | None = None):
        self.cache_dir = Path(cache_dir) if cache_dir else _DEFAULT_CACHE_DIR
        self.cache_dir.mkdir(parents=True, exist_ok=True)

    def write_pin(self, name: str, df: pd.DataFrame) -> Path:
        """Write a DataFrame as a versioned pin (Parquet file).

        Creates: ``<cache_dir>/<name>/data.parquet`` and a metadata JSON.
        """
        pin_dir = self.cache_dir / name
        pin_dir.mkdir(parents=True, exist_ok=True)

        data_path = pin_dir / "data.parquet"
        meta_path = pin_dir / "meta.json"

        df.to_parquet(data_path, index=False)

        meta = {
            "name": name,
            "rows": len(df),
            "columns": list(df.columns),
            "updated_at": datetime.utcnow().isoformat(),
        }
        meta_path.write_text(json.dumps(meta, indent=2))

        logger.info("Wrote pin '%s': %d rows → %s", name, len(df), data_path)
        return data_path

    def pin_exists(self, name: str) -> bool:
        return (self.cache_dir / name / "data.parquet").exists()

    def get_pin_meta(self, name: str) -> dict | None:
        meta_path = self.cache_dir / name / "meta.json"
        if meta_path.exists():
            return json.loads(meta_path.read_text())
        return None
