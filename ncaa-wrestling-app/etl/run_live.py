"""Live score fetcher.

Called by the Shiny app's reactive polling to get current scoreboard data.
Writes live scores to the pin cache for fast reads by the app.
"""

import logging
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

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
