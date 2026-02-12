"""Reusable score card component for displaying match results/live scores."""

from htmltools import Tag, tags


def score_card(
    away_team: str,
    home_team: str,
    away_score: int | None = None,
    home_score: int | None = None,
    away_rank: int | None = None,
    home_rank: int | None = None,
    status: str = "Upcoming",
    game_time: str = "",
    network: str = "",
    away_winner: bool = False,
    home_winner: bool = False,
) -> Tag:
    """Render a score card for a single match."""

    state_class = {
        "Live": "live",
        "Final": "final",
        "Upcoming": "upcoming",
    }.get(status, "upcoming")

    status_badge = ""
    if status == "Live":
        status_badge = tags.span(
            tags.span(class_="live-dot"),
            " LIVE",
            class_="live-badge",
        )
    elif status == "Final":
        status_badge = tags.span("FINAL", style="font-weight:700; font-size:0.8rem; color:#1a2744;")
    else:
        status_badge = tags.span(game_time, style="font-size:0.85rem; color:#7f8c8d;")

    def team_row(name: str, rank: int | None, score: int | None, is_winner: bool) -> Tag:
        rank_el = tags.span(f"#{rank} ", class_="team-rank") if rank else ""
        name_cls = "team-name winner" if is_winner else "team-name"
        score_cls = "team-score winner" if is_winner else "team-score"
        score_text = str(score) if score is not None else ""
        return tags.div(
            tags.div(rank_el, tags.span(name, class_=name_cls)),
            tags.span(score_text, class_=score_cls),
            class_="team-row",
        )

    info_parts = []
    if network:
        info_parts.append(tags.span(network))
    else:
        info_parts.append(tags.span(""))

    return tags.div(
        team_row(away_team, away_rank, away_score, away_winner),
        team_row(home_team, home_rank, home_score, home_winner),
        tags.div(status_badge, *info_parts, class_="game-info"),
        class_=f"score-card {state_class}",
    )


def score_cards_grid(cards: list[Tag]) -> Tag:
    """Wrap score cards in a responsive grid layout."""
    return tags.div(
        *cards,
        style="display:grid; grid-template-columns:repeat(auto-fill, minmax(300px, 1fr)); gap:0.75rem;",
    )
