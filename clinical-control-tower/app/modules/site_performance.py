"""
Site Performance & Ranking Module
====================================
Interactive site-level analytics with composite ranking,
geographic distribution, and drill-down capabilities.
"""

from shiny import ui, render, reactive
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from utils.data_loader import load_studies, load_sites, load_site_rankings
from utils.theme import COLORS, PLOTLY_TEMPLATE


def site_performance_ui():
    studies = load_studies()
    study_choices = {"All": "All Studies"}
    study_choices.update({row["study_id"]: f"{row['study_id']} - {row['study_name']}"
                          for _, row in studies.iterrows()})

    return ui.nav_panel(
        "Site Performance",
        ui.div(
            # Header
            ui.div(
                ui.h4("Site Performance & Ranking", class_="section-header"),
                ui.p("Composite site scoring powered by ML-driven ranking algorithms. "
                     "Sites are scored across enrollment velocity, data quality, protocol compliance, "
                     "and operational efficiency.",
                     style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem;"),
            ),

            # Posit callout
            ui.div(
                ui.div("Pins: Versioned Data Artifacts", class_="callout-title"),
                ui.div("Site rankings are computed daily via the Quarto ETL pipeline and stored as "
                       "versioned Pins on Posit Connect. Every historical ranking snapshot is preserved, "
                       "enabling trend analysis and auditability. Data scientists in Posit Workbench "
                       "can pull the latest rankings with a single line: "
                       "pins.board_connect().pin_read('site-rankings')",
                       class_="callout-body"),
                class_="posit-callout mb-4",
            ),

            # Filters
            ui.row(
                ui.column(12,
                    ui.div(
                        ui.row(
                            ui.column(4,
                                ui.input_select("site_study_filter", "Filter by Study",
                                                choices=study_choices, width="100%"),
                            ),
                            ui.column(3,
                                ui.input_select("site_region_filter", "Filter by Region",
                                                choices={"All": "All Regions",
                                                         "North America": "North America",
                                                         "Europe": "Europe",
                                                         "Asia-Pacific": "Asia-Pacific",
                                                         "Latin America": "Latin America",
                                                         "Africa": "Africa"},
                                                width="100%"),
                            ),
                            ui.column(3,
                                ui.input_select("site_tier_filter", "Filter by Tier",
                                                choices={"All": "All Tiers",
                                                         "Top Performer": "Top Performer",
                                                         "Good": "Good",
                                                         "Below Average": "Below Average",
                                                         "Underperforming": "Underperforming"},
                                                width="100%"),
                            ),
                            ui.column(2,
                                ui.input_numeric("site_top_n", "Show Top N",
                                                 value=25, min=5, max=100, step=5),
                            ),
                        ),
                        class_="filter-panel",
                    ),
                ),
                class_="mb-4",
            ),

            # KPI row
            ui.row(
                ui.column(3,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("sp_total_sites"), class_="value"),
                            ui.div("Sites in View", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(3,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("sp_avg_score"), class_="value"),
                            ui.div("Avg Composite Score", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(3,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("sp_top_performers"), class_="value"),
                            ui.div("Top Performers", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(3,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("sp_underperforming"), class_="value"),
                            ui.div("Underperforming", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Charts
            ui.row(
                ui.column(7,
                    ui.div(
                        ui.div("Site Ranking - Composite Scores", class_="card-header"),
                        ui.div(
                            ui.output_ui("site_ranking_chart_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(5,
                    ui.div(
                        ui.div("Performance Tier Distribution", class_="card-header"),
                        ui.div(
                            ui.output_ui("tier_chart_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Map and details
            ui.row(
                ui.column(6,
                    ui.div(
                        ui.div("Geographic Distribution", class_="card-header"),
                        ui.div(
                            ui.output_ui("site_map_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(6,
                    ui.div(
                        ui.div("Score Component Breakdown", class_="card-header"),
                        ui.div(
                            ui.output_ui("score_breakdown_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Detailed table
            ui.row(
                ui.column(12,
                    ui.div(
                        ui.div("Site Details", class_="card-header"),
                        ui.div(
                            ui.output_ui("site_detail_table_container"),
                            class_="card-body p-0",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            class_="p-4",
        ),
        icon=ui.tags.i(class_="fa-solid fa-ranking-star"),
    )


def site_performance_server(input, output, session):
    sites = load_sites()
    rankings = load_site_rankings()
    studies = load_studies()

    # Merge sites with rankings
    if len(rankings) > 0:
        merged = sites.merge(
            rankings[["site_id", "composite_rank_score", "rank_within_study",
                       "performance_tier", "enrollment_score", "quality_norm",
                       "screen_fail_score", "query_score", "deviation_score",
                       "activation_score"]],
            on="site_id", how="left"
        )
    else:
        merged = sites.copy()
        merged["composite_rank_score"] = 0.5
        merged["performance_tier"] = "Good"
        merged["rank_within_study"] = 1

    @reactive.calc
    def filtered_sites():
        df = merged.copy()

        if input.site_study_filter() != "All":
            df = df[df["study_id"] == input.site_study_filter()]

        if input.site_region_filter() != "All":
            df = df[df["region"] == input.site_region_filter()]

        if input.site_tier_filter() != "All":
            df = df[df["performance_tier"] == input.site_tier_filter()]

        return df.sort_values("composite_rank_score", ascending=False)

    # KPIs
    @render.text
    def sp_total_sites():
        return str(len(filtered_sites()))

    @render.text
    def sp_avg_score():
        df = filtered_sites()
        if len(df) > 0:
            return f"{df['composite_rank_score'].mean():.2f}"
        return "N/A"

    @render.text
    def sp_top_performers():
        df = filtered_sites()
        return str((df["performance_tier"] == "Top Performer").sum())

    @render.text
    def sp_underperforming():
        df = filtered_sites()
        return str((df["performance_tier"] == "Underperforming").sum())

    # Ranking chart
    @render.ui
    def site_ranking_chart_container():
        df = filtered_sites().head(input.site_top_n())

        if len(df) == 0:
            return ui.HTML("<p style='text-align: center; color: var(--text-secondary);'>No sites match the selected filters.</p>")

        df_sorted = df.sort_values("composite_rank_score", ascending=True).tail(25)

        tier_colors = {
            "Top Performer": COLORS["tier_top"],
            "Good": COLORS["tier_good"],
            "Below Average": COLORS["tier_below"],
            "Underperforming": COLORS["tier_under"],
        }

        colors = [tier_colors.get(t, "#999") for t in df_sorted["performance_tier"]]

        fig = go.Figure()
        fig.add_trace(go.Bar(
            y=df_sorted["site_id"],
            x=df_sorted["composite_rank_score"],
            orientation="h",
            marker_color=colors,
            text=df_sorted["composite_rank_score"].round(3),
            textposition="outside",
            textfont_size=10,
            hovertemplate=(
                "<b>%{y}</b><br>"
                "Score: %{x:.3f}<br>"
                "Country: %{customdata[0]}<br>"
                "Tier: %{customdata[1]}<extra></extra>"
            ),
            customdata=df_sorted[["country", "performance_tier"]].values,
        ))

        fig.update_layout(
            height=max(350, len(df_sorted) * 22),
            margin=dict(t=10, b=30, l=90, r=50),
            xaxis=dict(title="Composite Score", range=[0, 1], gridcolor="#E5E7EB"),
            yaxis=dict(tickfont_size=9),
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis", "margin"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Tier distribution
    @render.ui
    def tier_chart_container():
        df = filtered_sites()
        if len(df) == 0:
            return ui.HTML("<p style='text-align: center;'>No data.</p>")

        tier_counts = df["performance_tier"].value_counts()
        tier_order = ["Top Performer", "Good", "Below Average", "Underperforming"]
        tier_counts = tier_counts.reindex(tier_order).fillna(0)

        colors = [COLORS["tier_top"], COLORS["tier_good"], COLORS["tier_below"], COLORS["tier_under"]]

        fig = go.Figure(data=[go.Pie(
            labels=tier_counts.index.tolist(),
            values=tier_counts.values.tolist(),
            hole=0.5,
            marker_colors=colors,
            textinfo="label+percent",
            textfont_size=11,
            hovertemplate="%{label}: %{value} sites (%{percent})<extra></extra>",
        )])

        fig.update_layout(
            height=350,
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Geographic map
    @render.ui
    def site_map_container():
        df = filtered_sites()
        if len(df) == 0:
            return ui.HTML("<p style='text-align: center;'>No data.</p>")

        tier_colors_map = {
            "Top Performer": COLORS["tier_top"],
            "Good": COLORS["tier_good"],
            "Below Average": COLORS["tier_below"],
            "Underperforming": COLORS["tier_under"],
        }

        fig = go.Figure()

        for tier in ["Top Performer", "Good", "Below Average", "Underperforming"]:
            tier_df = df[df["performance_tier"] == tier]
            if len(tier_df) > 0:
                fig.add_trace(go.Scattergeo(
                    lat=tier_df["lat"],
                    lon=tier_df["lon"],
                    name=tier,
                    marker=dict(
                        size=7,
                        color=tier_colors_map.get(tier, "#999"),
                        opacity=0.7,
                        line=dict(width=0.5, color="white"),
                    ),
                    text=tier_df["site_id"] + " - " + tier_df["country"],
                    hovertemplate="<b>%{text}</b><br>Tier: " + tier + "<extra></extra>",
                ))

        fig.update_geos(
            showland=True, landcolor="#F5F5F5",
            showocean=True, oceancolor="#E8F4FD",
            showcountries=True, countrycolor="#D5D5D5",
            showframe=False,
            projection_type="natural earth",
        )

        fig.update_layout(
            height=380,
            margin=dict(t=10, b=10, l=10, r=10),
            legend=dict(orientation="h", yanchor="bottom", y=-0.05, xanchor="center", x=0.5, font_size=10),
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis", "margin"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Score breakdown radar
    @render.ui
    def score_breakdown_container():
        df = filtered_sites()
        if len(df) == 0 or "enrollment_score" not in df.columns:
            return ui.HTML("<p style='text-align: center;'>No data.</p>")

        score_cols = ["enrollment_score", "quality_norm", "screen_fail_score",
                      "query_score", "deviation_score", "activation_score"]
        labels = ["Enrollment", "Quality", "Screen\nSuccess", "Query\nRate", "Compliance", "Activation"]

        # Compare top vs bottom tier
        top = df[df["performance_tier"] == "Top Performer"]
        bottom = df[df["performance_tier"] == "Underperforming"]

        fig = go.Figure()

        if len(top) > 0:
            values = [top[c].mean() for c in score_cols]
            values.append(values[0])
            labels_r = labels + [labels[0]]
            fig.add_trace(go.Scatterpolar(
                r=values, theta=labels_r,
                fill="toself",
                fillcolor="rgba(27, 94, 32, 0.1)",
                line_color=COLORS["tier_top"],
                name="Top Performers",
            ))

        if len(bottom) > 0:
            values = [bottom[c].mean() for c in score_cols]
            values.append(values[0])
            labels_r = labels + [labels[0]]
            fig.add_trace(go.Scatterpolar(
                r=values, theta=labels_r,
                fill="toself",
                fillcolor="rgba(244, 67, 54, 0.1)",
                line_color=COLORS["tier_under"],
                name="Underperforming",
            ))

        # Overall average
        values = [df[c].mean() for c in score_cols]
        values.append(values[0])
        labels_r = labels + [labels[0]]
        fig.add_trace(go.Scatterpolar(
            r=values, theta=labels_r,
            line=dict(color=COLORS["chart_1"], dash="dash"),
            name="Portfolio Avg",
        ))

        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 1], gridcolor="#E5E7EB")),
            height=380,
            margin=dict(t=30, b=30, l=60, r=60),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5, font_size=10),
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis", "margin"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Detail table
    @render.ui
    def site_detail_table_container():
        df = filtered_sites().head(input.site_top_n())
        if len(df) == 0:
            return ui.HTML("<p style='text-align: center;'>No sites match filters.</p>")

        cols = ["site_id", "country", "investigator", "patients_enrolled",
                "enrollment_rate_per_month", "quality_score", "composite_rank_score",
                "performance_tier"]
        display = df[cols].copy()

        def tier_badge(t):
            colors = {
                "Top Performer": "signal-low",
                "Good": "signal-low",
                "Below Average": "signal-medium",
                "Underperforming": "signal-critical",
            }
            return f'<span class="signal-badge {colors.get(t, "")}">{t}</span>'

        display["performance_tier"] = display["performance_tier"].apply(tier_badge)
        display["composite_rank_score"] = display["composite_rank_score"].round(3)
        display["quality_score"] = display["quality_score"].round(3)

        display.columns = ["Site ID", "Country", "Investigator", "Enrolled",
                           "Rate/Mo", "Quality", "Composite", "Tier"]

        html = display.to_html(index=False, escape=False, classes="table table-sm table-hover mb-0")
        return ui.HTML(f'<div class="table-container" style="max-height: 400px; overflow-y: auto;">{html}</div>')
