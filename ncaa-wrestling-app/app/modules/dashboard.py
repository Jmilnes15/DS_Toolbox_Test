"""Dashboard page module — overview with stats, recent results, and rankings snapshot."""

from shiny import module, reactive, render, ui

from app.components.data_table import empty_state, render_dataframe_html
from app.components.value_boxes import rank_badge_html, movement_indicator
from app.utils.data_loader import (
    load_live_scores,
    load_rankings,
    load_schedule,
    load_standings,
    pin_updated_at,
)


@module.ui
def dashboard_ui():
    return ui.page_fluid(
        # Hero header
        ui.div(
            ui.h2("NCAA D1 Wrestling Tracker", style="margin:0; font-weight:700;"),
            ui.p("Your hub for rankings, scores, schedules, and brackets",
                 style="margin:0; color:#7f8c8d; font-size:0.95rem;"),
            style="margin-bottom:1.5rem;",
        ),
        # Summary value boxes
        ui.row(
            ui.column(3, ui.output_ui("vb_top_team")),
            ui.column(3, ui.output_ui("vb_teams_ranked")),
            ui.column(3, ui.output_ui("vb_live_matches")),
            ui.column(3, ui.output_ui("vb_upcoming")),
        ),
        ui.br(),
        # Two-column layout: Rankings + Recent Results
        ui.row(
            ui.column(
                6,
                ui.div(
                    ui.div("Top 10 Rankings", class_="card-header"),
                    ui.div(
                        ui.output_ui("top_rankings"),
                        class_="card-body",
                        style="padding:0;",
                    ),
                    class_="card",
                ),
            ),
            ui.column(
                6,
                ui.div(
                    ui.div("Recent Results", class_="card-header"),
                    ui.div(
                        ui.output_ui("recent_results"),
                        class_="card-body",
                        style="padding:0;",
                    ),
                    class_="card",
                ),
            ),
        ),
        ui.br(),
        # Conference standings preview
        ui.row(
            ui.column(
                12,
                ui.div(
                    ui.div("Conference Standings Preview", class_="card-header"),
                    ui.div(
                        ui.output_ui("standings_preview"),
                        class_="card-body",
                        style="padding:0;",
                    ),
                    class_="card",
                ),
            ),
        ),
    )


@module.server
def dashboard_server(input, output, session):

    @render.ui
    def vb_top_team():
        df = load_rankings()
        if not df.empty and "school" in df.columns:
            top = df.iloc[0]["school"]
            return ui.value_box(title="#1 Team", value=top, theme="bg-warning")
        return ui.value_box(title="#1 Team", value="—", theme="bg-secondary")

    @render.ui
    def vb_teams_ranked():
        df = load_rankings()
        count = len(df) if not df.empty else 0
        return ui.value_box(title="Teams Ranked", value=str(count), theme="bg-primary")

    @render.ui
    def vb_live_matches():
        df = load_live_scores()
        count = 0
        if not df.empty and "game_state" in df.columns:
            count = len(df[df["game_state"] == "live"])
        theme = "bg-danger" if count > 0 else "bg-secondary"
        return ui.value_box(title="Live Now", value=str(count), theme=theme)

    @render.ui
    def vb_upcoming():
        df = load_schedule()
        count = 0
        if not df.empty and "status" in df.columns:
            count = len(df[df["status"] == "Upcoming"])
        return ui.value_box(title="Upcoming", value=str(count), theme="bg-info")

    @render.ui
    def top_rankings():
        df = load_rankings()
        if df.empty:
            return empty_state("No rankings data")

        display = df.head(10).copy()
        if "rank" in display.columns:
            display[""] = display["rank"].apply(rank_badge_html)
        if "movement" in display.columns:
            display["Trend"] = display["movement"].apply(movement_indicator)

        rename = {"school": "School", "record": "Record", "points": "Pts"}
        display = display.rename(columns={k: v for k, v in rename.items() if k in display.columns})

        show = ["", "School", "Record", "Pts", "Trend"]
        show = [c for c in show if c in display.columns]
        return render_dataframe_html(display[show])

    @render.ui
    def recent_results():
        df = load_schedule()
        if df.empty:
            return empty_state("No recent results")

        results = df[df["status"] == "Final"].tail(10).copy()
        if results.empty:
            return empty_state("No recent results")

        def matchup(row):
            ar = f"#{int(row['away_rank'])} " if row.get("away_rank") else ""
            hr = f"#{int(row['home_rank'])} " if row.get("home_rank") else ""
            return f"{ar}{row['away_team']} @ {hr}{row['home_team']}"

        def score(row):
            if row.get("away_score") is not None and row.get("home_score") is not None:
                return f"{int(row['away_score'])}-{int(row['home_score'])}"
            return ""

        results["Matchup"] = results.apply(matchup, axis=1)
        results["Score"] = results.apply(score, axis=1)
        if "date" in results.columns:
            results["Date"] = results["date"].dt.strftime("%b %d").fillna("")

        return render_dataframe_html(results[["Date", "Matchup", "Score"]])

    @render.ui
    def standings_preview():
        df = load_standings()
        if df.empty:
            return empty_state("No standings data")

        # Show first conference only as preview
        if "conference" in df.columns:
            first_conf = df["conference"].iloc[0]
            preview = df[df["conference"] == first_conf].head(10).copy()
        else:
            preview = df.head(10).copy()

        rename = {
            "team": "Team",
            "conference": "Conference",
            "conf_wins": "Conf W",
            "conf_losses": "Conf L",
            "overall_wins": "W",
            "overall_losses": "L",
        }
        preview = preview.rename(columns={k: v for k, v in rename.items() if k in preview.columns})
        return render_dataframe_html(preview)
