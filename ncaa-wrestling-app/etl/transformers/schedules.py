"""Build a schedule DataFrame from scoreboard data across a date range."""

from datetime import date, timedelta

import pandas as pd

from etl.transformers.scores import classify_game_state


def build_schedule(games: list[dict]) -> pd.DataFrame:
    """Transform a list of raw game dicts (from scoreboard range) into a schedule.

    Each game dict is the inner ``game`` object from the scoreboard API,
    with an added ``_fetch_date`` field.
    """
    if not games:
        return _empty_schedule()

    rows = []
    for game in games:
        away = game.get("away", {})
        home = game.get("home", {})
        away_names = away.get("names", {})
        home_names = home.get("names", {})

        state = game.get("gameState", "pre")

        rows.append({
            "game_id": game.get("gameID", ""),
            "date": game.get("_fetch_date", ""),
            "start_time": game.get("startTime", ""),
            "start_time_epoch": game.get("startTimeEpoch", ""),
            "away_team": away_names.get("short", ""),
            "away_rank": _safe_int(away.get("rank")),
            "home_team": home_names.get("short", ""),
            "home_rank": _safe_int(home.get("rank")),
            "network": game.get("network", ""),
            "location": "",  # Not in scoreboard API; enriched later if available
            "status": classify_game_state(state),
            "away_score": _safe_int(away.get("score")),
            "home_score": _safe_int(home.get("score")),
            "title": game.get("title", ""),
            "url": game.get("url", ""),
        })

    df = pd.DataFrame(rows)
    df["date"] = pd.to_datetime(df["date"], errors="coerce")
    df = df.sort_values("date").reset_index(drop=True)
    return df


def get_upcoming_schedule(schedule_df: pd.DataFrame) -> pd.DataFrame:
    """Filter schedule to only upcoming (future) events."""
    if schedule_df.empty:
        return schedule_df
    today = pd.Timestamp(date.today())
    mask = schedule_df["date"] >= today
    return schedule_df[mask].reset_index(drop=True)


def get_recent_results(schedule_df: pd.DataFrame, days_back: int = 7) -> pd.DataFrame:
    """Filter schedule to recent completed events."""
    if schedule_df.empty:
        return schedule_df
    cutoff = pd.Timestamp(date.today() - timedelta(days=days_back))
    mask = (schedule_df["status"] == "Final") & (schedule_df["date"] >= cutoff)
    return schedule_df[mask].sort_values("date", ascending=False).reset_index(drop=True)


def _safe_int(val) -> int | None:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def _empty_schedule() -> pd.DataFrame:
    return pd.DataFrame(columns=[
        "game_id", "date", "start_time", "away_team", "away_rank",
        "home_team", "home_rank", "network", "location", "status",
        "away_score", "home_score", "title", "url",
    ])
