"""Transform raw NCAA API team stats and standings into clean DataFrames."""

import pandas as pd


def transform_team_stats(raw_rows: list[dict]) -> pd.DataFrame:
    """Transform raw team stat rows into a clean DataFrame.

    Handles dynamic column names from the NCAA API.
    """
    if not raw_rows:
        return _empty_team_stats()

    df = pd.DataFrame(raw_rows)

    # Normalize column names — NCAA API returns uppercase from HTML headers
    col_map = {}
    for col in df.columns:
        lower = col.strip().lower()
        if lower in ("rank", "#"):
            col_map[col] = "rank"
        elif lower in ("team", "school", "name"):
            col_map[col] = "team"
        elif lower in ("w", "wins"):
            col_map[col] = "wins"
        elif lower in ("l", "losses"):
            col_map[col] = "losses"
        elif lower in ("pct", "win pct", "winning percentage"):
            col_map[col] = "win_pct"
        elif lower in ("g", "gp", "games"):
            col_map[col] = "games"
        elif lower in ("falls",):
            col_map[col] = "falls"
        elif lower in ("tech falls", "tf"):
            col_map[col] = "tech_falls"
        elif lower in ("maj. dec.", "major decisions", "md"):
            col_map[col] = "major_decisions"
        else:
            col_map[col] = lower.replace(" ", "_").replace(".", "")

    df = df.rename(columns=col_map)

    # Convert numeric columns
    for col in ["rank", "wins", "losses", "games", "falls", "tech_falls", "major_decisions"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "win_pct" in df.columns:
        df["win_pct"] = pd.to_numeric(df["win_pct"].astype(str).str.replace("%", ""), errors="coerce")

    if "rank" in df.columns:
        df = df.sort_values("rank").reset_index(drop=True)

    return df


def transform_standings(raw: dict | None) -> pd.DataFrame:
    """Transform the standings API response into a flat DataFrame.

    Expected raw structure::

        {
            "data": [
                {
                    "conference": "Big Ten",
                    "standings": [
                        {"School": "Penn St.", "Conference W": "8", ...},
                    ]
                }
            ]
        }
    """
    if not raw or "data" not in raw:
        return _empty_standings()

    rows = []
    for conf_block in raw["data"]:
        conference = conf_block.get("conference", "Unknown")
        for team in conf_block.get("standings", []):
            row = {"conference": conference}
            for key, val in team.items():
                clean_key = key.strip().lower().replace(" ", "_")
                row[clean_key] = val
            rows.append(row)

    df = pd.DataFrame(rows)
    if df.empty:
        return _empty_standings()

    # Rename common columns
    rename_map = {
        "school": "team",
        "conference_w": "conf_wins",
        "conference_l": "conf_losses",
        "conference_pct": "conf_pct",
        "overall_w": "overall_wins",
        "overall_l": "overall_losses",
        "overall_pct": "overall_pct",
        "overall_streak": "streak",
    }
    df = df.rename(columns={k: v for k, v in rename_map.items() if k in df.columns})

    # Convert numerics
    for col in ["conf_wins", "conf_losses", "overall_wins", "overall_losses"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df


def transform_schools(raw_list: list[dict]) -> pd.DataFrame:
    """Transform the schools index into a DataFrame.

    Each item: {slug, name, long}
    """
    if not raw_list:
        return pd.DataFrame(columns=["slug", "name", "full_name"])

    df = pd.DataFrame(raw_list)
    df = df.rename(columns={"long": "full_name"})
    return df


def _empty_team_stats() -> pd.DataFrame:
    return pd.DataFrame(columns=["rank", "team", "wins", "losses", "win_pct"])


def _empty_standings() -> pd.DataFrame:
    return pd.DataFrame(columns=[
        "conference", "team", "conf_wins", "conf_losses",
        "overall_wins", "overall_losses",
    ])
