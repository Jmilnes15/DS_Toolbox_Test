"""
Risk Signal Detection Module
================================
Real-time risk monitoring with signal detection, severity tracking,
and mitigation workflows.
"""

from shiny import ui, render, reactive
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from utils.data_loader import load_studies, load_risk_signals, load_sites
from utils.theme import COLORS, PLOTLY_TEMPLATE


def risk_signals_ui():
    studies = load_studies()
    study_choices = {"All": "All Studies"}
    study_choices.update({row["study_id"]: row["study_id"] for _, row in studies.iterrows()})

    return ui.nav_panel(
        "Risk Signals",
        ui.div(
            # Header
            ui.div(
                ui.h4("Risk Signal Detection & Monitoring", class_="section-header"),
                ui.p("Automated risk detection algorithms continuously monitor trial operations, "
                     "flagging quality issues, enrollment risks, and compliance concerns before "
                     "they impact study timelines.",
                     style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem;"),
            ),

            # Posit callout
            ui.div(
                ui.div("Posit Connect: From Signal to Action", class_="callout-title"),
                ui.div("Risk detection algorithms run as scheduled Quarto jobs on Posit Connect. "
                       "When a critical signal is detected, Connect can trigger email alerts, "
                       "update Pins with the latest risk data, and refresh this dashboard — all "
                       "automatically. No separate alerting infrastructure needed.",
                       class_="callout-body"),
                class_="posit-callout mb-4",
            ),

            # Filters
            ui.row(
                ui.column(12,
                    ui.div(
                        ui.row(
                            ui.column(3,
                                ui.input_select("risk_study_filter", "Study",
                                                choices=study_choices, width="100%"),
                            ),
                            ui.column(3,
                                ui.input_select("risk_severity_filter", "Severity",
                                                choices={"All": "All", "Critical": "Critical",
                                                         "High": "High", "Medium": "Medium",
                                                         "Low": "Low"},
                                                width="100%"),
                            ),
                            ui.column(3,
                                ui.input_select("risk_status_filter", "Status",
                                                choices={"All": "All", "Open": "Open",
                                                         "Under Review": "Under Review",
                                                         "Mitigated": "Mitigated",
                                                         "Closed": "Closed"},
                                                width="100%"),
                            ),
                            ui.column(3,
                                ui.input_select("risk_category_filter", "Category",
                                                choices={"All": "All",
                                                         "enrollment": "Enrollment",
                                                         "quality": "Quality",
                                                         "compliance": "Compliance",
                                                         "operational": "Operational",
                                                         "supply": "Supply",
                                                         "strategic": "Strategic",
                                                         "regulatory": "Regulatory",
                                                         "financial": "Financial"},
                                                width="100%"),
                            ),
                        ),
                        class_="filter-panel",
                    ),
                ),
                class_="mb-4",
            ),

            # KPI row
            ui.row(
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("rs_total"), class_="value"),
                            ui.div("Total Signals", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("rs_critical"), class_="value",
                                   style="color: var(--danger);"),
                            ui.div("Critical", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("rs_high"), class_="value",
                                   style="color: var(--warning);"),
                            ui.div("High", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("rs_open"), class_="value"),
                            ui.div("Open / Under Review", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("rs_avg_days"), class_="value"),
                            ui.div("Avg Days Open", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("rs_mitigated"), class_="value",
                                   style="color: var(--success);"),
                            ui.div("Mitigated / Closed", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Charts
            ui.row(
                ui.column(6,
                    ui.div(
                        ui.div("Signals by Category & Severity", class_="card-header"),
                        ui.div(
                            ui.output_ui("signal_heatmap_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(6,
                    ui.div(
                        ui.div("Signal Status Pipeline", class_="card-header"),
                        ui.div(
                            ui.output_ui("signal_funnel_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Impact timeline
            ui.row(
                ui.column(12,
                    ui.div(
                        ui.div("Signal Impact Matrix", class_="card-header"),
                        ui.div(
                            ui.output_ui("impact_matrix_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Detail table
            ui.row(
                ui.column(12,
                    ui.div(
                        ui.div("Signal Details & Actions", class_="card-header"),
                        ui.div(
                            ui.output_ui("signal_detail_table_container"),
                            class_="card-body p-0",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            class_="p-4",
        ),
        icon=ui.tags.i(class_="fa-solid fa-triangle-exclamation"),
    )


def risk_signals_server(input, output, session):
    signals = load_risk_signals()

    @reactive.calc
    def filtered_signals():
        df = signals.copy()

        if input.risk_study_filter() != "All":
            df = df[df["study_id"] == input.risk_study_filter()]
        if input.risk_severity_filter() != "All":
            df = df[df["severity"] == input.risk_severity_filter()]
        if input.risk_status_filter() != "All":
            df = df[df["status"] == input.risk_status_filter()]
        if input.risk_category_filter() != "All":
            df = df[df["category"] == input.risk_category_filter()]

        return df

    # KPIs
    @render.text
    def rs_total():
        return str(len(filtered_signals()))

    @render.text
    def rs_critical():
        return str((filtered_signals()["severity"] == "Critical").sum())

    @render.text
    def rs_high():
        return str((filtered_signals()["severity"] == "High").sum())

    @render.text
    def rs_open():
        df = filtered_signals()
        return str(df["status"].isin(["Open", "Under Review"]).sum())

    @render.text
    def rs_avg_days():
        df = filtered_signals()
        if len(df) > 0:
            return f"{df['days_open'].mean():.0f}"
        return "0"

    @render.text
    def rs_mitigated():
        df = filtered_signals()
        return str(df["status"].isin(["Mitigated", "Closed"]).sum())

    # Heatmap
    @render.ui
    def signal_heatmap_container():
        df = filtered_signals()
        if len(df) == 0:
            return ui.HTML("<p style='text-align: center; color: var(--text-secondary);'>No signals match filters.</p>")

        pivot = df.groupby(["category", "severity"]).size().reset_index(name="count")
        pivot_wide = pivot.pivot(index="category", columns="severity", values="count").fillna(0)

        sev_order = ["Critical", "High", "Medium", "Low"]
        for s in sev_order:
            if s not in pivot_wide.columns:
                pivot_wide[s] = 0
        pivot_wide = pivot_wide[sev_order]

        fig = go.Figure(data=go.Heatmap(
            z=pivot_wide.values,
            x=sev_order,
            y=pivot_wide.index.tolist(),
            colorscale=[[0, "#F5F5F5"], [0.5, "#FFB74D"], [1.0, "#C62828"]],
            text=pivot_wide.values.astype(int),
            texttemplate="%{text}",
            textfont_size=14,
            hovertemplate="Category: %{y}<br>Severity: %{x}<br>Count: %{z}<extra></extra>",
            showscale=False,
        ))

        fig.update_layout(
            height=300,
            margin=dict(t=10, b=30, l=100, r=20),
            xaxis=dict(side="top"),
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis", "margin"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Status funnel
    @render.ui
    def signal_funnel_container():
        df = filtered_signals()
        if len(df) == 0:
            return ui.HTML("<p style='text-align: center;'>No data.</p>")

        status_order = ["Open", "Under Review", "Mitigated", "Closed"]
        status_counts = df["status"].value_counts().reindex(status_order).fillna(0)

        colors = [COLORS["danger"], COLORS["warning"], COLORS["chart_1"], COLORS["success"]]

        fig = go.Figure(go.Funnel(
            y=status_counts.index.tolist(),
            x=status_counts.values.tolist(),
            marker_color=colors,
            textinfo="value+percent initial",
            textfont_size=13,
            hovertemplate="%{y}: %{x} signals<extra></extra>",
        ))

        fig.update_layout(
            height=300,
            margin=dict(t=10, b=10, l=10, r=10),
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis", "margin"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Impact matrix (bubble chart)
    @render.ui
    def impact_matrix_container():
        df = filtered_signals()
        if len(df) == 0:
            return ui.HTML("<p style='text-align: center;'>No data.</p>")

        severity_num = {"Critical": 4, "High": 3, "Medium": 2, "Low": 1}
        df_plot = df.copy()
        df_plot["severity_num"] = df_plot["severity"].map(severity_num)

        sev_colors = {
            "Critical": COLORS["risk_critical"],
            "High": COLORS["risk_high"],
            "Medium": COLORS["risk_medium"],
            "Low": COLORS["risk_low"],
        }

        fig = go.Figure()

        for sev in ["Critical", "High", "Medium", "Low"]:
            sev_df = df_plot[df_plot["severity"] == sev]
            if len(sev_df) > 0:
                fig.add_trace(go.Scatter(
                    x=sev_df["days_open"],
                    y=sev_df["impact_score"],
                    mode="markers",
                    name=sev,
                    marker=dict(
                        size=sev_df["n_affected_sites"] * 4 + 8,
                        color=sev_colors[sev],
                        opacity=0.7,
                        line=dict(width=1, color="white"),
                    ),
                    text=sev_df["signal_name"],
                    hovertemplate=(
                        "<b>%{text}</b><br>"
                        "Days Open: %{x}<br>"
                        "Impact: %{y:.2f}<br>"
                        "Study: %{customdata}<extra></extra>"
                    ),
                    customdata=sev_df["study_id"],
                ))

        fig.update_layout(
            height=350,
            margin=dict(t=10, b=40, l=50, r=20),
            xaxis=dict(title="Days Open", gridcolor="#E5E7EB"),
            yaxis=dict(title="Impact Score", range=[0, 1.05], gridcolor="#E5E7EB"),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis", "margin"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Detail table
    @render.ui
    def signal_detail_table_container():
        df = filtered_signals().sort_values(["severity", "days_open"], ascending=[True, False])

        if len(df) == 0:
            return ui.HTML("<p style='text-align: center;'>No signals match filters.</p>")

        cols = ["signal_id", "study_id", "signal_name", "category", "severity",
                "status", "days_open", "n_affected_sites", "recommended_action", "assigned_to"]
        display = df[cols].copy()

        def severity_badge(s):
            cls = {"Critical": "signal-critical", "High": "signal-high",
                   "Medium": "signal-medium", "Low": "signal-low"}.get(s, "")
            return f'<span class="signal-badge {cls}">{s}</span>'

        display["severity"] = display["severity"].apply(severity_badge)
        display.columns = ["Signal", "Study", "Name", "Category", "Severity",
                           "Status", "Days Open", "Sites", "Action", "Assigned"]

        html = display.to_html(index=False, escape=False, classes="table table-sm table-hover mb-0")
        return ui.HTML(f'<div class="table-container" style="max-height: 450px; overflow-y: auto;">{html}</div>')
