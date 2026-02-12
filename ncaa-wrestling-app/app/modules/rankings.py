"""Rankings page module — team rankings with filtering and movement indicators."""

from shiny import module, reactive, render, ui

from app.components.data_table import empty_state, render_dataframe_html
from app.components.value_boxes import movement_indicator, rank_badge_html
from app.utils.data_loader import load_rankings, pin_updated_at


@module.ui
def rankings_ui():
    return ui.page_fluid(
        ui.row(
            ui.column(
                12,
                ui.h3("D1 Wrestling Team Rankings"),
                ui.p(
                    ui.output_text("rankings_updated"),
                    style="color:#7f8c8d; font-size:0.85rem;",
                ),
            ),
        ),
        ui.row(
            ui.column(
                {"class": "col-12 col-lg-3 mb-3"},
                ui.div(
                    ui.input_numeric("top_n", "Show Top N", value=25, min=5, max=100, step=5),
                    ui.input_text("search_team", "Search Team", placeholder="e.g. Penn St."),
                    class_="filter-section",
                ),
            ),
            ui.column(
                {"class": "col-12 col-lg-9"},
                ui.output_ui("rankings_table"),
            ),
        ),
    )


@module.server
def rankings_server(input, output, session):

    @reactive.calc
    def rankings_data():
        df = load_rankings()
        if df.empty:
            return df

        # Apply search filter
        search = input.search_team().strip()
        if search:
            mask = df["school"].str.contains(search, case=False, na=False)
            df = df[mask]

        # Apply top N
        top_n = input.top_n() or 25
        df = df.head(top_n)

        return df

    @render.text
    def rankings_updated():
        ts = pin_updated_at("rankings")
        return f"Last updated: {ts}"

    @render.ui
    def rankings_table():
        df = rankings_data()
        if df.empty:
            return empty_state("No rankings data available")

        # Add display columns
        display = df.copy()

        if "rank" in display.columns:
            display[""] = display["rank"].apply(rank_badge_html)
        if "movement" in display.columns:
            display["Trend"] = display["movement"].apply(movement_indicator)
        if "school" in display.columns:
            display = display.rename(columns={"school": "School"})
        if "record" in display.columns:
            display = display.rename(columns={"record": "Record"})
        if "points" in display.columns:
            display = display.rename(columns={"points": "Points"})
        if "previous_rank" in display.columns:
            display = display.rename(columns={"previous_rank": "Prev"})

        # Select display columns
        show_cols = ["", "School", "Record", "Points", "Prev", "Trend"]
        show_cols = [c for c in show_cols if c in display.columns]
        display = display[show_cols]

        return render_dataframe_html(display)
