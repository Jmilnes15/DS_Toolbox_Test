"""Reusable value box helpers for the dashboard."""

from shiny import ui


def stat_value_box(title: str, value: str | int, theme: str = "primary") -> ui.Tag:
    """Create a themed value box for dashboard stats."""
    theme_map = {
        "primary": "bg-primary",
        "secondary": "bg-warning",
        "success": "bg-success",
        "danger": "bg-danger",
        "info": "bg-info",
    }
    return ui.value_box(
        title=title,
        value=str(value),
        theme=theme_map.get(theme, "bg-primary"),
    )


def movement_indicator(movement: int) -> str:
    """Return an HTML string showing rank movement with arrow."""
    if movement > 0:
        return f'<span class="movement-up">&#9650; {movement}</span>'
    elif movement < 0:
        return f'<span class="movement-down">&#9660; {abs(movement)}</span>'
    else:
        return '<span class="movement-same">&#8212;</span>'


def rank_badge_html(rank: int | None) -> str:
    """Return HTML for a circular rank badge."""
    if rank is None:
        return ""
    if rank <= 5:
        cls = "rank-badge top-5"
    elif rank <= 10:
        cls = "rank-badge top-10"
    else:
        cls = "rank-badge top-25"
    return f'<span class="{cls}">{rank}</span>'
