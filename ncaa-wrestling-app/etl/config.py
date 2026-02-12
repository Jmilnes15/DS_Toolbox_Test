"""Configuration for the ETL data pipeline."""

from app.utils.constants import (
    NCAA_API_BASE_URL,
    OPENTW_API_BASE_URL,
    PIN_BOARD_NAME,
)

# NCAA API configuration
NCAA_API = {
    "base_url": NCAA_API_BASE_URL,
    "rate_limit_per_second": 5,
    "timeout_seconds": 30,
    "retry_attempts": 3,
}

# OpenTW API configuration
OPENTW_API = {
    "base_url": OPENTW_API_BASE_URL,
    "timeout_seconds": 30,
    "retry_attempts": 3,
}

# Web scraping targets
SCRAPE_TARGETS = {
    "wrestlestat": {
        "base_url": "https://www.wrestlestat.com",
        "rankings_path": "/rankings",
        "enabled": True,
    },
    "intermat": {
        "base_url": "https://intermatwrestle.com",
        "rankings_path": "/rankings",
        "enabled": True,
    },
    "espn_schedule": {
        "base_url": "https://www.espn.com",
        "schedule_path": "/college-sports/wrestling/schedule",
        "enabled": True,
    },
}

# Pins configuration
PINS_CONFIG = {
    "board_name": PIN_BOARD_NAME,
    "versioned": True,
}

# ETL schedule (cron expressions for Posit Connect)
SCHEDULE = {
    "daily_etl": "0 6 * * *",       # 6:00 AM ET daily
    "schedule_refresh": "0 6,18 * * *",  # 6:00 AM and 6:00 PM ET
}
