"""Brackets page module — NCAA tournament bracket visualization."""

from shiny import module, reactive, render, ui

from app.components.data_table import empty_state
from app.utils.constants import WEIGHT_CLASSES, WEIGHT_CLASS_LABELS


@module.ui
def brackets_ui():
    wt_choices = {str(w): WEIGHT_CLASS_LABELS[w] for w in WEIGHT_CLASSES}
    return ui.page_fluid(
        ui.row(
            ui.column(
                12,
                ui.h3("NCAA Tournament Brackets"),
                ui.p(
                    "Bracket data is available during NCAA Championship tournaments.",
                    style="color:#7f8c8d; font-size:0.85rem;",
                ),
            ),
        ),
        ui.row(
            ui.column(
                {"class": "col-12 col-lg-3 mb-3"},
                ui.div(
                    ui.input_select(
                        "weight_class",
                        "Weight Class",
                        choices=wt_choices,
                        selected="125",
                    ),
                    ui.input_select(
                        "bracket_round",
                        "Round",
                        choices={
                            "all": "All Rounds",
                            "r32": "Round of 32",
                            "r16": "Round of 16",
                            "qf": "Quarterfinals",
                            "sf": "Semifinals",
                            "finals": "Finals",
                            "cons": "Consolations",
                        },
                        selected="all",
                    ),
                    ui.input_action_button(
                        "refresh_brackets",
                        "Refresh Brackets",
                        class_="btn btn-primary btn-sm w-100",
                    ),
                    class_="filter-section",
                ),
            ),
            ui.column(
                {"class": "col-12 col-lg-9"},
                ui.output_ui("bracket_view"),
            ),
        ),
    )


@module.server
def brackets_server(input, output, session):

    @reactive.calc
    def bracket_data():
        input.refresh_brackets()

        # In production, this would fetch from OpenTW API or pin cache.
        # For now, return sample bracket structure.
        from app.utils.data_loader import load_brackets
        df = load_brackets()
        return df

    @render.ui
    def bracket_view():
        df = bracket_data()
        if df.empty:
            return _bracket_placeholder(input.weight_class())

        wt = int(input.weight_class())
        label = WEIGHT_CLASS_LABELS.get(wt, f"{wt} lbs")
        return ui.div(
            ui.h4(f"{label} Bracket"),
            ui.p("Bracket visualization will render during tournament season.",
                 style="color:#7f8c8d;"),
        )


def _bracket_placeholder(weight_class: str) -> ui.Tag:
    """Show a placeholder bracket when no data is available."""
    wt = int(weight_class) if weight_class.isdigit() else 125
    label = WEIGHT_CLASS_LABELS.get(wt, f"{wt} lbs")

    sample_matchups = [
        ("(1) Top Seed", "(32) Opening Round"),
        ("(16) Mid Seed", "(17) Mid Seed"),
        ("(8) High Seed", "(25) Qualifier"),
        ("(9) Competitive", "(24) Qualifier"),
    ]

    match_elements = []
    for w1, w2 in sample_matchups:
        match_elements.append(
            ui.div(
                ui.div(
                    ui.div(w1, class_="wrestler"),
                    ui.div(w2, class_="wrestler"),
                    class_="bracket-match",
                ),
            )
        )

    return ui.div(
        ui.div(
            ui.div("Championship Bracket", class_="card-header"),
            ui.div(
                ui.h5(f"{label}", style="margin-bottom:1rem;"),
                ui.p(
                    "Bracket data is populated during the NCAA Championship tournament. "
                    "Check back during tournament season for live bracket updates.",
                    style="color:#7f8c8d; font-size:0.9rem;",
                ),
                ui.hr(),
                ui.h6("Bracket Preview Format", style="color:#2a3f6a; margin-bottom:0.75rem;"),
                ui.div(
                    ui.div(*match_elements, class_="bracket-round"),
                    class_="bracket-container",
                    style="display:flex;",
                ),
                class_="card-body",
            ),
            class_="card",
        ),
    )
