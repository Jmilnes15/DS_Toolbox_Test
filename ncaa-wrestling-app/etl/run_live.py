"""Live score fetcher.

Fetches today's scoreboard from the NCAA API and writes it to the pins board.
Designed to run as a frequently-scheduled job on Posit Connect (via Quarto).
"""

import logging
import sys
from datetime import date
from pathlib import Path

_project_root = str(Path(__file__).resolve().parent.parent)
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

from etl.ncaa_api import NCAAApiClient
from etl.pin_writer import PinWriter
from etl.transformers.scores import transform_scoreboard

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def fetch_live_scores() -> int:
    """Fetch today's scoreboard and write to the live_scores pin.

    Returns the number of games found.
    """
    client = NCAAApiClient()
    writer = PinWriter()

    raw = client.get_scoreboard(date.today())
    df = transform_scoreboard(raw)
    writer.write_pin("live_scores", df)

    live_count = len(df[df["game_state"] == "live"]) if not df.empty and "game_state" in df.columns else 0
    logger.info("Live scores: %d total games, %d live now", len(df), live_count)
    return len(df)


if __name__ == "__main__":
    fetch_live_scores()
