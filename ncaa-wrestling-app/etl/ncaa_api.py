"""NCAA API client for fetching wrestling data.

Wraps the henrygd/ncaa-api which mirrors NCAA.com URL paths and returns JSON.
Public instance: https://ncaa-api.henrygd.me
Rate limit: 5 requests/second per IP.
"""

import logging
import time
from datetime import date, datetime, timedelta
from typing import Any

import httpx

logger = logging.getLogger(__name__)

NCAA_API_BASE = "https://ncaa-api.henrygd.me"
SPORT = "wrestling"
DIV = "d1"
_RATE_LIMIT_DELAY = 0.22  # ~4.5 req/s to stay under the 5/s limit


class NCAAApiClient:
    """Client for the NCAA wrestling API."""

    def __init__(self, base_url: str = NCAA_API_BASE, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self._last_request_time: float = 0.0

    def _throttle(self) -> None:
        elapsed = time.monotonic() - self._last_request_time
        if elapsed < _RATE_LIMIT_DELAY:
            time.sleep(_RATE_LIMIT_DELAY - elapsed)

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict | list | None:
        url = f"{self.base_url}{path}"
        self._throttle()
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url, params=params)
                self._last_request_time = time.monotonic()
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as exc:
            logger.warning("HTTP %s for %s", exc.response.status_code, url)
            return None
        except httpx.RequestError as exc:
            logger.error("Request failed for %s: %s", url, exc)
            return None

    # ------------------------------------------------------------------
    # Scoreboard / Live Scores
    # ------------------------------------------------------------------

    def get_scoreboard(self, target_date: date | None = None, conference: str = "all-conf") -> dict | None:
        """Fetch the scoreboard for a given date.

        Returns the full scoreboard JSON with a ``games`` list.
        """
        d = target_date or date.today()
        path = f"/scoreboard/{SPORT}/{DIV}/{d.year}/{d.month:02d}/{d.day:02d}/{conference}"
        return self._get(path)

    def get_scoreboard_range(self, start: date, end: date) -> list[dict]:
        """Fetch scoreboards across a date range and merge the games lists."""
        all_games: list[dict] = []
        current = start
        while current <= end:
            data = self.get_scoreboard(current)
            if data and "games" in data:
                for g in data["games"]:
                    game = g.get("game", g)
                    game["_fetch_date"] = current.isoformat()
                    all_games.append(game)
            current += timedelta(days=1)
        return all_games

    # ------------------------------------------------------------------
    # Rankings
    # ------------------------------------------------------------------

    def get_rankings(self, poll: str = "current") -> dict | None:
        """Fetch team rankings (e.g. NWCA Coaches Poll).

        Returns ``{sport, title, updated, page, pages, data: [...]}``.
        """
        path = f"/rankings/{SPORT}/{DIV}/{poll}"
        return self._get(path)

    # ------------------------------------------------------------------
    # Standings
    # ------------------------------------------------------------------

    def get_standings(self, year: int | None = None) -> dict | None:
        """Fetch conference standings for the given season year."""
        y = year or datetime.now().year
        path = f"/standings/{SPORT}/{DIV}/{y}"
        return self._get(path)

    # ------------------------------------------------------------------
    # Stats
    # ------------------------------------------------------------------

    def get_team_stats(self, stat_id: int = 170, page: int = 1) -> dict | None:
        """Fetch team-level statistics.

        Known wrestling stat IDs:
          170 — Winning Percentage (default)
        """
        path = f"/stats/{SPORT}/{DIV}/current/team/{stat_id}"
        return self._get(path, params={"page": page})

    def get_all_team_stats(self, stat_id: int = 170) -> list[dict]:
        """Fetch all pages of a team stat and return the merged data list."""
        first_page = self.get_team_stats(stat_id, page=1)
        if not first_page:
            return []
        rows = list(first_page.get("data", []))
        total_pages = int(first_page.get("pages", 1))
        for p in range(2, total_pages + 1):
            page_data = self.get_team_stats(stat_id, page=p)
            if page_data:
                rows.extend(page_data.get("data", []))
        return rows

    def get_individual_stats(self, stat_id: int = 171, page: int = 1) -> dict | None:
        """Fetch individual wrestler statistics.

        Known wrestling stat IDs:
          171 — Wins (default)
        """
        path = f"/stats/{SPORT}/{DIV}/current/individual/{stat_id}"
        return self._get(path, params={"page": page})

    def get_all_individual_stats(self, stat_id: int = 171) -> list[dict]:
        """Fetch all pages of an individual stat and return the merged data list."""
        first_page = self.get_individual_stats(stat_id, page=1)
        if not first_page:
            return []
        rows = list(first_page.get("data", []))
        total_pages = int(first_page.get("pages", 1))
        for p in range(2, total_pages + 1):
            page_data = self.get_individual_stats(stat_id, page=p)
            if page_data:
                rows.extend(page_data.get("data", []))
        return rows

    # ------------------------------------------------------------------
    # Schools
    # ------------------------------------------------------------------

    def get_schools(self) -> list[dict]:
        """Fetch the full NCAA schools index.

        Returns a list of ``{slug, name, long}`` dicts.
        """
        data = self._get("/schools-index")
        return data if isinstance(data, list) else []

    # ------------------------------------------------------------------
    # Game Detail
    # ------------------------------------------------------------------

    def get_game_boxscore(self, game_id: str) -> dict | None:
        """Fetch box score for a specific game."""
        return self._get(f"/game/{game_id}/boxscore")

    def get_game_play_by_play(self, game_id: str) -> dict | None:
        """Fetch play-by-play for a specific game."""
        return self._get(f"/game/{game_id}/play-by-play")

    def get_game_scoring(self, game_id: str) -> dict | None:
        """Fetch scoring summary for a specific game."""
        return self._get(f"/game/{game_id}/scoring-summary")

    def get_game_team_stats(self, game_id: str) -> dict | None:
        """Fetch team stats for a specific game."""
        return self._get(f"/game/{game_id}/team-stats")
