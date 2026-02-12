"""Write processed DataFrames to a Posit Connect pins board.

On Posit Connect:
    Uses ``pins.board_connect()`` which auto-detects the server URL and API key
    from the ``CONNECT_SERVER`` and ``CONNECT_API_KEY`` environment variables
    (injected automatically when content runs on Connect).

For local development:
    Falls back to ``pins.board_folder()`` using a local ``pin_cache/`` directory.
    Set CONNECT_SERVER + CONNECT_API_KEY env vars to test against a real board.
"""

import logging
import os
from pathlib import Path

import pandas as pd
import pins

logger = logging.getLogger(__name__)

# Pin name prefix — keeps our pins namespaced on shared Connect boards
PIN_PREFIX = "ncaa_wrestling"

_LOCAL_CACHE_DIR = Path(__file__).resolve().parent.parent / "pin_cache"


def _is_on_connect() -> bool:
    """Detect whether we're running on Posit Connect."""
    return bool(os.environ.get("CONNECT_SERVER"))


def get_board() -> pins.BaseBoard:
    """Return the appropriate pins board for the current environment.

    On Connect: ``board_connect()`` using env vars.
    Locally: ``board_folder()`` writing to ``pin_cache/``.
    """
    if _is_on_connect():
        logger.info("Using Posit Connect pins board")
        return pins.board_connect(
            server_url=os.environ["CONNECT_SERVER"],
            api_key=os.environ.get("CONNECT_API_KEY", ""),
            allow_pickle_read=False,
        )
    else:
        _LOCAL_CACHE_DIR.mkdir(parents=True, exist_ok=True)
        logger.info("Using local pins board at %s", _LOCAL_CACHE_DIR)
        return pins.board_folder(_LOCAL_CACHE_DIR, allow_pickle_read=False)


def _pin_name(name: str) -> str:
    """Build the full pin name with prefix."""
    return f"{PIN_PREFIX}/{name}"


class PinWriter:
    """Write DataFrames to the pins board."""

    def __init__(self):
        self.board = get_board()

    def write_pin(self, name: str, df: pd.DataFrame) -> None:
        """Write a DataFrame as a pin.

        Args:
            name: Short pin name (e.g. ``"rankings"``). Will be prefixed
                  with ``ncaa_wrestling/``.
            df: The DataFrame to persist.
        """
        full_name = _pin_name(name)
        self.board.pin_write(df, full_name, type="parquet")
        logger.info("Wrote pin '%s': %d rows", full_name, len(df))

    def pin_exists(self, name: str) -> bool:
        """Check if a pin exists on the board."""
        full_name = _pin_name(name)
        try:
            existing = self.board.pin_list()
            return full_name in existing
        except Exception:
            return False

    def get_pin_meta(self, name: str) -> dict | None:
        """Read pin metadata (version info, created time)."""
        full_name = _pin_name(name)
        try:
            meta = self.board.pin_meta(full_name)
            return {
                "name": full_name,
                "created": str(meta.created),
                "version": str(meta.version),
            }
        except Exception:
            return None
