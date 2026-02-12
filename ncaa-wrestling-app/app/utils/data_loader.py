"""Load pinned data for the Shiny app.

On Posit Connect:
    Reads from ``pins.board_connect()`` — the same board the ETL jobs write to.

For local development:
    Reads from ``pins.board_folder()`` at ``pin_cache/``.

Falls back to empty DataFrames when data hasn't been written yet.
"""

import logging
import os
from pathlib import Path

import pandas as pd
import pins

logger = logging.getLogger(__name__)

PIN_PREFIX = "ncaa_wrestling"
_LOCAL_CACHE_DIR = Path(__file__).resolve().parent.parent.parent / "pin_cache"

# Cache the board instance so we don't re-create it on every read
_board: pins.BaseBoard | None = None


def _get_board() -> pins.BaseBoard:
    """Get or create the pins board (cached)."""
    global _board
    if _board is not None:
        return _board

    if os.environ.get("CONNECT_SERVER"):
        logger.info("Data loader: using Posit Connect pins board")
        _board = pins.board_connect(
            server_url=os.environ["CONNECT_SERVER"],
            api_key=os.environ.get("CONNECT_API_KEY", ""),
            allow_pickle_read=False,
        )
    else:
        _LOCAL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("Data loader: using local pins board at %s", _LOCAL_CACHE_DIR)
        _board = pins.board_folder(_LOCAL_CACHE_DIR, allow_pickle_read=False)

    return _board


def _pin_name(name: str) -> str:
    return f"{PIN_PREFIX}/{name}"


def read_pin(name: str) -> pd.DataFrame:
    """Read a pinned DataFrame. Returns an empty DataFrame if the pin doesn't exist."""
    full_name = _pin_name(name)
    try:
        board = _get_board()
        return board.pin_read(full_name)
    except Exception as exc:
        logger.warning("Could not read pin '%s': %s — returning empty DataFrame", full_name, exc)
        return pd.DataFrame()


def pin_updated_at(name: str) -> str:
    """Return the last-updated timestamp for a pin, or 'Never' if unavailable."""
    full_name = _pin_name(name)
    try:
        board = _get_board()
        meta = board.pin_meta(full_name)
        return str(meta.created)
    except Exception:
        return "Never"


# ------------------------------------------------------------------
# Convenience loaders used by the Shiny modules
# ------------------------------------------------------------------

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
