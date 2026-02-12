"""Daily ETL orchestrator.

Fetches rankings, standings, team stats, individual stats, schools, and
schedule data from the NCAA API, transforms them, and writes to the pin cache.

Designed to run as a scheduled job on Posit Connect (via Quarto) or manually.
"""

import logging
import sys
from datetime import date, timedelta
from pathlib import Path

# Ensure project root is on the path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from etl.ncaa_api import NCAAApiClient
from etl.pin_writer import PinWriter
from etl.transformers.rankings import transform_team_rankings
from etl.transformers.scores import transform_scoreboard
from etl.transformers.schedules import build_schedule
from etl.transformers.teams import transform_team_stats, transform_standings, transform_schools

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)


def run_daily_etl() -> dict[str, int]:
    """Execute the full daily ETL pipeline. Returns row counts per pin."""
    client = NCAAApiClient()
    writer = PinWriter()
    results: dict[str, int] = {}

    # --- Rankings ---
    logger.info("Fetching rankings...")
    raw_rankings = client.get_rankings("current")
    df_rankings = transform_team_rankings(raw_rankings)
    writer.write_pin("rankings", df_rankings)
    results["rankings"] = len(df_rankings)

    # --- Team Stats ---
    logger.info("Fetching team stats...")
    raw_team_stats = client.get_all_team_stats(stat_id=170)
    df_team_stats = transform_team_stats(raw_team_stats)
    writer.write_pin("team_stats", df_team_stats)
    results["team_stats"] = len(df_team_stats)

    # --- Individual Stats ---
    logger.info("Fetching individual stats...")
    raw_ind_stats = client.get_all_individual_stats(stat_id=171)
    df_ind_stats = transform_team_stats(raw_ind_stats)  # Same shape handler
    writer.write_pin("individual_stats", df_ind_stats)
    results["individual_stats"] = len(df_ind_stats)

    # --- Standings ---
    logger.info("Fetching standings...")
    raw_standings = client.get_standings()
    df_standings = transform_standings(raw_standings)
    writer.write_pin("standings", df_standings)
    results["standings"] = len(df_standings)

    # --- Schools ---
    logger.info("Fetching schools index...")
    raw_schools = client.get_schools()
    df_schools = transform_schools(raw_schools)
    writer.write_pin("schools", df_schools)
    results["schools"] = len(df_schools)

    # --- Schedule (past 7 days + next 30 days) ---
    logger.info("Fetching schedule (past 7 days + next 30 days)...")
    start = date.today() - timedelta(days=7)
    end = date.today() + timedelta(days=30)
    raw_games = client.get_scoreboard_range(start, end)
    df_schedule = build_schedule(raw_games)
    writer.write_pin("schedule", df_schedule)
    results["schedule"] = len(df_schedule)

    logger.info("Daily ETL complete. Results: %s", results)
    return results


if __name__ == "__main__":
    run_daily_etl()
