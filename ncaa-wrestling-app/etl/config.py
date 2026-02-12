"""Configuration for the ETL data pipeline."""

# NCAA API configuration
NCAA_API = {
    "base_url": "https://ncaa-api.henrygd.me",
    "rate_limit_per_second": 5,
    "timeout_seconds": 30,
    "retry_attempts": 3,
}

# OpenTW API configuration
OPENTW_API = {
    "base_url": "https://opentw-api.henrygd.me",
    "timeout_seconds": 30,
    "retry_attempts": 3,
}

# Pins configuration
PINS_CONFIG = {
    "board_dir": "pin_cache",
    "versioned": True,
}

# ETL schedule (cron expressions for Posit Connect)
SCHEDULE = {
    "daily_etl": "0 6 * * *",       # 6:00 AM ET daily
    "live_scores": "*/1 * * * *",    # Every minute during events
    "schedule_refresh": "0 6,18 * * *",  # 6:00 AM and 6:00 PM ET
}
