"""Constants used across the NCAA Wrestling Tracker app."""

WEIGHT_CLASSES = [125, 133, 141, 149, 157, 165, 174, 184, 197, 285]

NCAA_API_BASE_URL = "https://ncaa-api.henrygd.me"

SPORT = "wrestling"
DIVISION = "d1"

# Scoreboard endpoint pattern
SCOREBOARD_URL = f"{NCAA_API_BASE_URL}/scoreboard/{SPORT}/{DIVISION}"

# Rankings endpoint pattern
RANKINGS_URL = f"{NCAA_API_BASE_URL}/rankings/{SPORT}/{DIVISION}"

# Stats endpoint patterns
TEAM_STATS_URL = f"{NCAA_API_BASE_URL}/stats/{SPORT}/{DIVISION}/current/team"
INDIVIDUAL_STATS_URL = f"{NCAA_API_BASE_URL}/stats/{SPORT}/{DIVISION}/current/individual"

# Standings endpoint
STANDINGS_URL = f"{NCAA_API_BASE_URL}/standings/{SPORT}/{DIVISION}"

# Schools index
SCHOOLS_URL = f"{NCAA_API_BASE_URL}/schools-index"

# OpenTW API (TrackWrestling)
OPENTW_API_BASE_URL = "https://opentw-api.example.com"  # Replace with actual deployment URL

# Refresh intervals (seconds)
LIVE_SCORE_REFRESH_INTERVAL = 60
BRACKET_REFRESH_INTERVAL = 120

# Pin board name
PIN_BOARD_NAME = "ncaa_wrestling"

# Pin names
PIN_RANKINGS = "rankings"
PIN_TEAM_STATS = "team_stats"
PIN_INDIVIDUAL_STATS = "individual_stats"
PIN_STANDINGS = "standings"
PIN_SCHEDULE = "schedule"
PIN_SCHOOLS = "schools"
PIN_LIVE_SCORES = "live_scores"
PIN_BRACKETS = "brackets"
