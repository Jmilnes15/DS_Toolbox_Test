"""
Clinical Control Tower
========================
A Shiny for Python application demonstrating how Posit's ecosystem
powers end-to-end clinical trial operational analytics.

Deploy to Posit Connect with:
    rsconnect deploy shiny ./app/ --title "Clinical Control Tower"
"""

import sys
import os

# Ensure the app directory is on the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from shiny import App, ui, render

from modules.executive_dashboard import executive_dashboard_ui, executive_dashboard_server
from modules.enrollment_forecasting import enrollment_forecasting_ui, enrollment_forecasting_server
from modules.site_performance import site_performance_ui, site_performance_server
from modules.risk_signals import risk_signals_ui, risk_signals_server
from modules.how_it_works import how_it_works_ui, how_it_works_server
from utils.theme import APP_CSS

# ============================================================
# UI
# ============================================================
app_ui = ui.page_navbar(
    # Navigation pages
    executive_dashboard_ui(),
    enrollment_forecasting_ui(),
    site_performance_ui(),
    risk_signals_ui(),
    how_it_works_ui(),

    # Navbar config
    title=ui.div(
        ui.tags.span(
            "CLINICAL CONTROL TOWER",
            style="font-weight: 800; font-size: 1.05rem; letter-spacing: 0.05em;",
        ),
        ui.tags.span(
            " | Powered by Posit",
            style="font-weight: 400; font-size: 0.8rem; opacity: 0.7; margin-left: 0.5rem;",
        ),
        style="display: flex; align-items: baseline;",
    ),
    id="main_nav",
    fluid=True,
    navbar_options=ui.navbar_options(bg="#1B2A4A", theme="dark"),
    header=ui.tags.head(
        # Font Awesome
        ui.tags.link(
            rel="stylesheet",
            href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css",
        ),
        # Google Fonts
        ui.tags.link(
            href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap",
            rel="stylesheet",
        ),
        # Custom CSS
        ui.tags.style(APP_CSS),
    ),
    footer=ui.div(
        ui.div(
            ui.tags.span(
                "Clinical Control Tower Demo",
                style="font-weight: 600;",
            ),
            " | Built with ",
            ui.tags.span("Shiny for Python", style="font-weight: 600; color: var(--secondary);"),
            " | Deployed on ",
            ui.tags.span("Posit Connect", style="font-weight: 600; color: var(--secondary);"),
            " | Data is simulated for demonstration purposes",
            style=(
                "text-align: center; padding: 0.75rem; font-size: 0.8rem; "
                "color: var(--text-secondary); border-top: 1px solid var(--border); "
                "background: white;"
            ),
        ),
    ),
)


# ============================================================
# Server
# ============================================================
def server(input, output, session):
    executive_dashboard_server(input, output, session)
    enrollment_forecasting_server(input, output, session)
    site_performance_server(input, output, session)
    risk_signals_server(input, output, session)
    how_it_works_server(input, output, session)


# ============================================================
# App
# ============================================================
app = App(app_ui, server)
