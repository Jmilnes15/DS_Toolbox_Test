"""NCAA D1 Wrestling Tracker — Shiny for Python application.

Main entry point that assembles the multi-page app with navbar navigation.

Deployment:
    rsconnect deploy shiny --entrypoint app/app.py ncaa-wrestling-app/

Environment variables (set in Connect content settings):
    CONNECT_SERVER   — auto-injected by Posit Connect
    CONNECT_API_KEY  — your Connect API key (for reading pins)
"""

import sys
from pathlib import Path

# Ensure project root is on sys.path so all imports resolve on Connect.
# On Connect the working directory is the content bundle root, which is
# the ``ncaa-wrestling-app/`` directory.
_project_root = Path(__file__).resolve().parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from shiny import App, ui

from app.modules.dashboard import dashboard_server, dashboard_ui
from app.modules.rankings import rankings_server, rankings_ui
from app.modules.schedule import schedule_server, schedule_ui
from app.modules.teams import teams_server, teams_ui
from app.modules.live_scores import live_scores_server, live_scores_ui
from app.modules.brackets import brackets_server, brackets_ui
from app.modules.how_it_works import how_it_works_server, how_it_works_ui

app_ui = ui.page_navbar(
    # Dashboard
    ui.nav_panel(
        "Dashboard",
        dashboard_ui("dashboard"),
    ),
    # Rankings
    ui.nav_panel(
        "Rankings",
        rankings_ui("rankings"),
    ),
    # Schedule
    ui.nav_panel(
        "Schedule",
        schedule_ui("schedule"),
    ),
    # Teams
    ui.nav_panel(
        "Teams",
        teams_ui("teams"),
    ),
    # Live Scores
    ui.nav_panel(
        "Live Scores",
        live_scores_ui("live_scores"),
    ),
    # Brackets
    ui.nav_panel(
        "Brackets",
        brackets_ui("brackets"),
    ),
    # Separator + How It Works
    ui.nav_spacer(),
    ui.nav_panel(
        "How It Works",
        how_it_works_ui("how_it_works"),
    ),
    title=ui.div(
        ui.span("NCAA Wrestling Tracker", style="font-weight:700;"),
        style="display:flex; align-items:center; gap:0.5rem;",
    ),
    id="main_nav",
    theme=ui.Theme("flatly"),
    header=ui.head_content(
        ui.tags.meta(name="viewport", content="width=device-width, initial-scale=1"),
        ui.include_css(Path(__file__).parent / "styles.css"),
    ),
    footer=ui.div(
        "NCAA D1 Wrestling Tracker | Data from NCAA.com via ncaa-api",
        class_="app-footer",
    ),
)


def server(input, output, session):
    """Main server function — delegates to page modules."""
    dashboard_server("dashboard")
    rankings_server("rankings")
    schedule_server("schedule")
    teams_server("teams")
    live_scores_server("live_scores")
    brackets_server("brackets")
    how_it_works_server("how_it_works")


app = App(app_ui, server)
