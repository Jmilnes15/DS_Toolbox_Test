"""Live Scores page module — real-time scoreboard with auto-refresh."""

from shiny import module, reactive, render, ui

from app.components.data_table import empty_state
from app.components.score_card import score_card, score_cards_grid
from app.utils.data_loader import load_live_scores, pin_updated_at


@module.ui
def live_scores_ui():
    return ui.page_fluid(
        ui.row(
            ui.column(
                {"class": "col-12 col-md-8 mb-2"},
                ui.h3("Live Scores"),
                ui.p(
                    ui.output_text("live_updated"),
                    style="color:#7f8c8d; font-size:0.85rem;",
                ),
            ),
            ui.column(
                {"class": "col-12 col-md-4 mb-2"},
                ui.div(
                    ui.input_action_button(
                        "refresh_btn",
                        "Refresh Scores",
                        class_="btn btn-primary btn-sm",
                    ),
                    ui.input_select(
                        "status_filter",
                        "",
                        choices={"all": "All Games", "live": "Live Now", "final": "Final",
                                 "upcoming": "Upcoming"},
                        selected="all",
                        width="100%",
                    ),
                    class_="d-flex flex-wrap gap-2 align-items-end justify-content-md-end",
                ),
            ),
        ),
        # Summary stats
        ui.row(
            ui.column(4, ui.output_ui("live_count_box"), {"class": "col-4 mb-2"}),
            ui.column(4, ui.output_ui("final_count_box"), {"class": "col-4 mb-2"}),
            ui.column(4, ui.output_ui("upcoming_count_box"), {"class": "col-4 mb-2"}),
            style="margin-bottom:1rem;",
        ),
        # Score cards
        ui.output_ui("score_cards"),
    )


@module.server
def live_scores_server(input, output, session):

    @reactive.calc
    def live_data():
        # Re-read on refresh button click
        input.refresh_btn()
        return load_live_scores()

    @reactive.calc
    def filtered_data():
        df = live_data()
        if df.empty:
            return df

        status = input.status_filter()
        if status != "all" and "game_state" in df.columns:
            df = df[df["game_state"].str.lower() == status]

        return df

    @render.text
    def live_updated():
        ts = pin_updated_at("live_scores")
        return f"Last refreshed: {ts}"

    @render.ui
    def live_count_box():
        df = live_data()
        count = len(df[df["game_state"] == "live"]) if not df.empty and "game_state" in df.columns else 0
        return ui.value_box(
            title="Live Now",
            value=str(count),
            theme="bg-danger" if count > 0 else "bg-secondary",
        )

    @render.ui
    def final_count_box():
        df = live_data()
        count = len(df[df["game_state"] == "final"]) if not df.empty and "game_state" in df.columns else 0
        return ui.value_box(title="Final", value=str(count), theme="bg-primary")

    @render.ui
    def upcoming_count_box():
        df = live_data()
        count = len(df[df["game_state"] == "pre"]) if not df.empty and "game_state" in df.columns else 0
        return ui.value_box(title="Upcoming", value=str(count), theme="bg-info")

    @render.ui
    def score_cards():
        from app.components.score_card import score_card as sc
        from etl.transformers.scores import classify_game_state

        df = filtered_data()
        if df.empty:
            return empty_state("No games today")

        cards = []
        for _, row in df.iterrows():
            status = classify_game_state(row.get("game_state", "pre"))
            cards.append(
                sc(
                    away_team=row.get("away_team", ""),
                    home_team=row.get("home_team", ""),
                    away_score=row.get("away_score"),
                    home_score=row.get("home_score"),
                    away_rank=row.get("away_rank"),
                    home_rank=row.get("home_rank"),
                    status=status,
                    game_time=row.get("start_time", ""),
                    network=row.get("network", ""),
                    away_winner=bool(row.get("away_winner", False)),
                    home_winner=bool(row.get("home_winner", False)),
                )
            )

        return score_cards_grid(cards)
