"""Schedule page module — upcoming matches and recent results."""

from shiny import module, reactive, render, ui

from app.components.data_table import empty_state, render_dataframe_html
from app.components.value_boxes import rank_badge_html
from app.utils.data_loader import load_schedule, pin_updated_at


@module.ui
def schedule_ui():
    return ui.page_fluid(
        ui.row(
            ui.column(
                12,
                ui.h3("D1 Wrestling Schedule & Results"),
                ui.p(
                    ui.output_text("schedule_updated"),
                    style="color:#7f8c8d; font-size:0.85rem;",
                ),
            ),
        ),
        ui.row(
            ui.column(
                {"class": "col-12 col-lg-3 mb-3"},
                ui.div(
                    ui.input_select(
                        "view_mode",
                        "View",
                        choices={"all": "All", "upcoming": "Upcoming", "results": "Results"},
                        selected="all",
                    ),
                    ui.input_text("search_schedule", "Search Team", placeholder="e.g. Iowa"),
                    ui.input_select(
                        "network_filter",
                        "Network",
                        choices={"all": "All Networks", "espn": "ESPN", "btn": "Big Ten Network",
                                 "flo": "FloWrestling"},
                        selected="all",
                    ),
                    class_="filter-section",
                ),
            ),
            ui.column(
                {"class": "col-12 col-lg-9"},
                ui.output_ui("schedule_table"),
            ),
        ),
    )


@module.server
def schedule_server(input, output, session):

    @reactive.calc
    def schedule_data():
        df = load_schedule()
        if df.empty:
            return df

        # View mode filter
        mode = input.view_mode()
        if mode == "upcoming":
            df = df[df["status"] == "Upcoming"]
        elif mode == "results":
            df = df[df["status"] == "Final"]

        # Search filter
        search = input.search_schedule().strip()
        if search:
            mask = (
                df["away_team"].str.contains(search, case=False, na=False)
                | df["home_team"].str.contains(search, case=False, na=False)
            )
            df = df[mask]

        # Network filter
        net = input.network_filter()
        if net != "all":
            net_map = {"espn": "ESPN", "btn": "Big Ten", "flo": "Flo"}
            pattern = net_map.get(net, net)
            df = df[df["network"].str.contains(pattern, case=False, na=False)]

        return df

    @render.text
    def schedule_updated():
        ts = pin_updated_at("schedule")
        return f"Last updated: {ts}"

    @render.ui
    def schedule_table():
        df = schedule_data()
        if df.empty:
            return empty_state("No scheduled events found")

        display = df.copy()

        # Format matchup column
        def matchup_str(row):
            away_rank = f"#{int(row['away_rank'])} " if row.get("away_rank") else ""
            home_rank = f"#{int(row['home_rank'])} " if row.get("home_rank") else ""
            return f"{away_rank}{row['away_team']}  @  {home_rank}{row['home_team']}"

        display["Matchup"] = display.apply(matchup_str, axis=1)

        # Format score
        def score_str(row):
            if row.get("status") == "Final" and row.get("away_score") is not None:
                return f"{int(row['away_score'])} - {int(row['home_score'])}"
            return ""

        display["Score"] = display.apply(score_str, axis=1)

        # Format date
        if "date" in display.columns:
            display["Date"] = display["date"].dt.strftime("%b %d, %Y").fillna("")

        display = display.rename(columns={
            "start_time": "Time",
            "network": "Network",
            "status": "Status",
        })

        show_cols = ["Date", "Matchup", "Score", "Time", "Network", "Status"]
        show_cols = [c for c in show_cols if c in display.columns]
        display = display[show_cols]

        return render_dataframe_html(display, max_rows=50)
