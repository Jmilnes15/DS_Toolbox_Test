"""Teams page module — conference standings and team stats."""

from shiny import module, reactive, render, ui

from app.components.data_table import empty_state, render_dataframe_html
from app.utils.data_loader import load_standings, load_team_stats, pin_updated_at


@module.ui
def teams_ui():
    return ui.page_fluid(
        ui.row(
            ui.column(
                12,
                ui.h3("D1 Wrestling Teams"),
                ui.p(
                    ui.output_text("teams_updated"),
                    style="color:#7f8c8d; font-size:0.85rem;",
                ),
            ),
        ),
        ui.row(
            ui.column(
                3,
                ui.div(
                    ui.input_select(
                        "view_type",
                        "View",
                        choices={"standings": "Conference Standings", "stats": "Team Stats"},
                        selected="standings",
                    ),
                    ui.input_select(
                        "conference_filter",
                        "Conference",
                        choices={"all": "All Conferences"},
                        selected="all",
                    ),
                    ui.input_text("search_team", "Search Team", placeholder="e.g. Ohio St."),
                    class_="filter-section",
                ),
            ),
            ui.column(
                9,
                ui.output_ui("teams_table"),
            ),
        ),
    )


@module.server
def teams_server(input, output, session):

    @reactive.effect
    def _update_conference_choices():
        df = load_standings()
        if not df.empty and "conference" in df.columns:
            confs = sorted(df["conference"].dropna().unique().tolist())
            choices = {"all": "All Conferences"}
            choices.update({c: c for c in confs})
            ui.update_select("conference_filter", choices=choices)

    @reactive.calc
    def standings_data():
        df = load_standings()
        if df.empty:
            return df

        conf = input.conference_filter()
        if conf != "all":
            df = df[df["conference"] == conf]

        search = input.search_team().strip()
        if search:
            team_col = "team" if "team" in df.columns else df.columns[1] if len(df.columns) > 1 else None
            if team_col:
                df = df[df[team_col].str.contains(search, case=False, na=False)]

        return df

    @reactive.calc
    def stats_data():
        df = load_team_stats()
        if df.empty:
            return df

        search = input.search_team().strip()
        if search:
            team_col = "team" if "team" in df.columns else None
            if team_col:
                df = df[df[team_col].str.contains(search, case=False, na=False)]

        return df

    @render.text
    def teams_updated():
        ts = pin_updated_at("standings")
        return f"Last updated: {ts}"

    @render.ui
    def teams_table():
        view = input.view_type()

        if view == "standings":
            df = standings_data()
            if df.empty:
                return empty_state("No standings data available")

            display = df.copy()
            rename_map = {
                "conference": "Conference",
                "team": "Team",
                "conf_wins": "Conf W",
                "conf_losses": "Conf L",
                "overall_wins": "W",
                "overall_losses": "L",
                "streak": "Streak",
            }
            display = display.rename(columns={k: v for k, v in rename_map.items() if k in display.columns})
            return render_dataframe_html(display, max_rows=100)

        else:
            df = stats_data()
            if df.empty:
                return empty_state("No team stats data available")

            display = df.copy()
            rename_map = {
                "rank": "Rank",
                "team": "Team",
                "wins": "W",
                "losses": "L",
                "win_pct": "Win %",
                "games": "GP",
            }
            display = display.rename(columns={k: v for k, v in rename_map.items() if k in display.columns})
            return render_dataframe_html(display)
