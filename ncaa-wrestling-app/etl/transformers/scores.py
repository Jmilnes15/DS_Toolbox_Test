"""Transform raw NCAA API scoreboard data into clean DataFrames."""

from datetime import datetime

import pandas as pd


def transform_scoreboard(raw: dict | None) -> pd.DataFrame:
    """Transform scoreboard JSON into a clean events/scores DataFrame.

    Expected raw structure::

        {
            "games": [
                {
                    "game": {
                        "gameID": "6154104",
                        "away": {"score": "12", "names": {"short": "Iowa", ...},
                                 "rank": "1", "winner": false, ...},
                        "home": {"score": "24", "names": {"short": "Penn St.", ...},
                                 "rank": "2", "winner": true, ...},
                        "gameState": "final",
                        "startDate": "02-01-2025",
                        "startTime": "7:00PM ET",
                        "startTimeEpoch": "...",
                        "network": "ESPN",
                        "finalMessage": "FINAL",
                        "title": "Iowa Penn St.",
                        "currentPeriod": "FINAL",
                        "contestClock": "0:00",
                        "url": "/game/6154104"
                    }
                }
            ]
        }
    """
    if not raw or "games" not in raw:
        return _empty_scoreboard()

    rows = []
    for entry in raw["games"]:
        game = entry.get("game", entry)
        away = game.get("away", {})
        home = game.get("home", {})
        away_names = away.get("names", {})
        home_names = home.get("names", {})

        row = {
            "game_id": game.get("gameID", ""),
            "game_state": game.get("gameState", ""),
            "start_date": _parse_date(game.get("startDate", "")),
            "start_time": game.get("startTime", ""),
            "start_time_epoch": game.get("startTimeEpoch", ""),
            "network": game.get("network", ""),
            "final_message": game.get("finalMessage", ""),
            "current_period": game.get("currentPeriod", ""),
            "contest_clock": game.get("contestClock", ""),
            "title": game.get("title", ""),
            "url": game.get("url", ""),
            # Away team
            "away_team": away_names.get("short", ""),
            "away_team_full": away_names.get("full", ""),
            "away_team_seo": away_names.get("seo", ""),
            "away_score": _safe_int(away.get("score", "")),
            "away_rank": _safe_int(away.get("rank", "")),
            "away_record": away.get("description", ""),
            "away_winner": away.get("winner", False),
            "away_conference": _get_conference(away),
            # Home team
            "home_team": home_names.get("short", ""),
            "home_team_full": home_names.get("full", ""),
            "home_team_seo": home_names.get("seo", ""),
            "home_score": _safe_int(home.get("score", "")),
            "home_rank": _safe_int(home.get("rank", "")),
            "home_record": home.get("description", ""),
            "home_winner": home.get("winner", False),
            "home_conference": _get_conference(home),
        }
        rows.append(row)

    df = pd.DataFrame(rows)
    return df


def classify_game_state(state: str) -> str:
    """Map raw gameState to a display-friendly status."""
    state = (state or "").lower().strip()
    if state == "final":
        return "Final"
    elif state == "live":
        return "Live"
    elif state in ("pre", ""):
        return "Upcoming"
    return state.title()


def _parse_date(raw: str) -> str:
    """Parse 'MM-DD-YYYY' into 'YYYY-MM-DD' ISO format."""
    if not raw:
        return ""
    try:
        dt = datetime.strptime(raw, "%m-%d-%Y")
        return dt.strftime("%Y-%m-%d")
    except ValueError:
        return raw


def _get_conference(team_data: dict) -> str:
    conferences = team_data.get("conferences", [])
    if conferences:
        return conferences[0].get("conferenceName", "")
    return ""


def _safe_int(val) -> int | None:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def _empty_scoreboard() -> pd.DataFrame:
    return pd.DataFrame(columns=[
        "game_id", "game_state", "start_date", "start_time", "network",
        "away_team", "away_score", "away_rank",
        "home_team", "home_score", "home_rank",
    ])
