"""OpenTW API client for fetching TrackWrestling tournament and bracket data.

The OpenTW API is a middleware that parses TrackWrestling into structured JSON.
GitHub: https://github.com/vehbiu/opentw-api
"""

import logging
from typing import Any

import httpx

logger = logging.getLogger(__name__)

OPENTW_BASE = "https://opentw-api.henrygd.me"


class OpenTWClient:
    """Client for the OpenTW (TrackWrestling) API."""

    def __init__(self, base_url: str = OPENTW_BASE, timeout: float = 30.0):
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout

    def _get(self, path: str, params: dict[str, Any] | None = None) -> dict | list | None:
        url = f"{self.base_url}{path}"
        try:
            with httpx.Client(timeout=self.timeout) as client:
                resp = client.get(url, params=params)
                resp.raise_for_status()
                return resp.json()
        except httpx.HTTPStatusError as exc:
            logger.warning("HTTP %s for %s", exc.response.status_code, url)
            return None
        except httpx.RequestError as exc:
            logger.error("Request failed for %s: %s", url, exc)
            return None

    def get_tournament(self, tournament_type: str, tournament_id: str) -> dict | None:
        """Fetch tournament details.

        Args:
            tournament_type: Type of tournament (e.g. "collegiate", "open").
            tournament_id: The TrackWrestling tournament ID.
        """
        return self._get(f"/tournaments/{tournament_type}/{tournament_id}")

    def get_tournament_matches(self, tournament_type: str, tournament_id: str) -> list | None:
        """Fetch match assignments and statuses for a tournament."""
        return self._get(f"/tournaments/{tournament_type}/{tournament_id}/matches")

    def get_tournament_brackets(self, tournament_type: str, tournament_id: str) -> list | None:
        """Fetch bracket data for a tournament."""
        return self._get(f"/tournaments/{tournament_type}/{tournament_id}/brackets")
