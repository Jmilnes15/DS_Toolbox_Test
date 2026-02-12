"""Constants used across the NCAA Wrestling Tracker app."""

WEIGHT_CLASSES = [125, 133, 141, 149, 157, 165, 174, 184, 197, 285]

WEIGHT_CLASS_LABELS = {
    125: "125 lbs",
    133: "133 lbs",
    141: "141 lbs",
    149: "149 lbs",
    157: "157 lbs",
    165: "165 lbs",
    174: "174 lbs",
    184: "184 lbs",
    197: "197 lbs",
    285: "285 lbs (HWT)",
}

NCAA_API_BASE_URL = "https://ncaa-api.henrygd.me"
SPORT = "wrestling"
DIVISION = "d1"

# Endpoint patterns
SCOREBOARD_URL = f"{NCAA_API_BASE_URL}/scoreboard/{SPORT}/{DIVISION}"
RANKINGS_URL = f"{NCAA_API_BASE_URL}/rankings/{SPORT}/{DIVISION}"
TEAM_STATS_URL = f"{NCAA_API_BASE_URL}/stats/{SPORT}/{DIVISION}/current/team"
INDIVIDUAL_STATS_URL = f"{NCAA_API_BASE_URL}/stats/{SPORT}/{DIVISION}/current/individual"
STANDINGS_URL = f"{NCAA_API_BASE_URL}/standings/{SPORT}/{DIVISION}"
SCHOOLS_URL = f"{NCAA_API_BASE_URL}/schools-index"
GAME_URL = f"{NCAA_API_BASE_URL}/game"

# Known stat IDs for wrestling on NCAA.com
TEAM_STAT_IDS = {
    "winning_pct": 170,
}
INDIVIDUAL_STAT_IDS = {
    "wins": 171,
}

# OpenTW API (TrackWrestling wrapper)
OPENTW_API_BASE_URL = "https://opentw-api.henrygd.me"

# Refresh intervals (seconds)
LIVE_SCORE_REFRESH_INTERVAL = 60
BRACKET_REFRESH_INTERVAL = 120
DASHBOARD_REFRESH_INTERVAL = 120

# Pin board / data cache
PIN_BOARD_DIR = "ncaa_wrestling_pins"
PIN_RANKINGS = "rankings"
PIN_TEAM_STATS = "team_stats"
PIN_INDIVIDUAL_STATS = "individual_stats"
PIN_STANDINGS = "standings"
PIN_SCHEDULE = "schedule"
PIN_SCHOOLS = "schools"
PIN_LIVE_SCORES = "live_scores"
PIN_BRACKETS = "brackets"
PIN_EVENTS = "events"

# Conferences for filtering
CONFERENCES = [
    "Big Ten", "Big 12", "ACC", "EIWA", "MAC",
    "SoCon", "PAC-12", "EWL", "Independent",
]

# Broadcast channels
BROADCAST_CHANNELS = [
    "ESPN", "ESPN2", "ESPNU", "ESPN+",
    "Big Ten Network", "B1G+",
    "FloWrestling", "ACC Network",
]

# Current season
CURRENT_SEASON_YEAR = 2026
