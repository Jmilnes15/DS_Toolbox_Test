"""Transform raw NCAA API ranking data into clean DataFrames."""

import pandas as pd


def transform_team_rankings(raw: dict | None) -> pd.DataFrame:
    """Transform the rankings API response into a clean DataFrame.

    Expected raw structure::

        {
            "sport": "Wrestling",
            "title": "...",
            "updated": "...",
            "data": [
                {"RANK": "1", "SCHOOL": "Penn St. (16)", "POINTS": "400",
                 "PREVIOUS": "1", "RECORD": "15-0"},
                ...
            ]
        }

    Returns a DataFrame with columns:
        rank, school, votes, points, previous_rank, record, wins, losses, movement
    """
    if not raw or "data" not in raw:
        return _empty_team_rankings()

    rows = []
    for item in raw["data"]:
        school_raw = item.get("SCHOOL", item.get("School", ""))
        school, votes = _parse_school_votes(school_raw)
        rank = _safe_int(item.get("RANK", item.get("Rank", "")))
        previous = _safe_int(item.get("PREVIOUS", item.get("Previous", "")))
        record = item.get("RECORD", item.get("Record", ""))
        wins, losses = _parse_record(record)
        points = _safe_int(item.get("POINTS", item.get("Points", "")))

        movement = (previous - rank) if (previous and rank) else 0

        rows.append({
            "rank": rank,
            "school": school,
            "votes": votes,
            "points": points,
            "previous_rank": previous,
            "record": record,
            "wins": wins,
            "losses": losses,
            "movement": movement,
        })

    df = pd.DataFrame(rows)
    if not df.empty:
        df = df.sort_values("rank").reset_index(drop=True)
    return df


def _parse_school_votes(raw: str) -> tuple[str, int | None]:
    """Parse 'Penn St. (16)' into ('Penn St.', 16)."""
    raw = raw.strip()
    if "(" in raw and raw.endswith(")"):
        idx = raw.rfind("(")
        school = raw[:idx].strip()
        votes_str = raw[idx + 1:-1].strip()
        try:
            return school, int(votes_str)
        except ValueError:
            return school, None
    return raw, None


def _parse_record(record: str) -> tuple[int | None, int | None]:
    """Parse '15-0' into (15, 0)."""
    if "-" in record:
        parts = record.split("-")
        try:
            return int(parts[0].strip()), int(parts[1].strip())
        except (ValueError, IndexError):
            pass
    return None, None


def _safe_int(val: str | int | None) -> int | None:
    if val is None or val == "":
        return None
    try:
        return int(val)
    except (ValueError, TypeError):
        return None


def _empty_team_rankings() -> pd.DataFrame:
    return pd.DataFrame(columns=[
        "rank", "school", "votes", "points",
        "previous_rank", "record", "wins", "losses", "movement",
    ])
