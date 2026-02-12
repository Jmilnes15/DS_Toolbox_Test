"""Reusable data table rendering helpers."""

import pandas as pd
from shiny import ui


def render_dataframe_html(df: pd.DataFrame, max_rows: int = 100) -> ui.Tag:
    """Render a pandas DataFrame as a styled HTML table.

    This avoids the overhead of great-tables for simple tabular display.
    """
    if df.empty:
        return ui.div(
            ui.p("No data available.", style="text-align:center; color:#7f8c8d; padding:2rem;"),
        )

    display_df = df.head(max_rows)
    html_str = display_df.to_html(
        index=False,
        classes="dataframe table table-striped table-hover",
        escape=False,
        border=0,
    )
    return ui.HTML(html_str)


def empty_state(message: str = "No data available") -> ui.Tag:
    """Render an empty state placeholder."""
    return ui.div(
        ui.div(
            ui.h4(message, style="color:#7f8c8d;"),
            ui.p("Run the ETL pipeline to fetch data, or check back later.",
                 style="color:#95a5a6; font-size:0.9rem;"),
            style="text-align:center; padding:3rem;",
        ),
        class_="card",
    )
