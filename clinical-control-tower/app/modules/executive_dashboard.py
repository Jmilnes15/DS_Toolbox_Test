"""
Executive Dashboard Module
============================
Portfolio-level view of all clinical trials with KPIs,
enrollment progress, risk overview, and study-level drill-down.
"""

from shiny import ui, render, reactive, module
from shinywidgets import render_plotly
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

from utils.data_loader import load_studies, load_sites, load_kpis, load_risk_signals
from utils.theme import COLORS, PLOTLY_TEMPLATE, APP_CSS


def executive_dashboard_ui():
    return ui.nav_panel(
        "Executive Dashboard",
        ui.div(
            # KPI Row
            ui.row(
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("kpi_total_studies"), class_="value"),
                            ui.div("Active Studies", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("kpi_total_enrolled"), class_="value"),
                            ui.div("Patients Enrolled", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("kpi_enrollment_pct"), class_="value"),
                            ui.div("Overall Enrollment", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("kpi_active_sites"), class_="value"),
                            ui.div("Active Sites", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("kpi_open_signals"), class_="value"),
                            ui.div("Open Signals", class_="label"),
                            ui.div(ui.output_ui("kpi_critical_badge"), class_="trend"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(2,
                    ui.div(
                        ui.div(
                            ui.div(ui.output_text("kpi_budget_util"), class_="value"),
                            ui.div("Budget Utilization", class_="label"),
                            class_="kpi-metric",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Charts Row 1
            ui.row(
                ui.column(8,
                    ui.div(
                        ui.div("Portfolio Enrollment Progress", class_="card-header"),
                        ui.div(
                            ui.output_ui("enrollment_chart_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(4,
                    ui.div(
                        ui.div("Risk Distribution", class_="card-header"),
                        ui.div(
                            ui.output_ui("risk_dist_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Charts Row 2
            ui.row(
                ui.column(5,
                    ui.div(
                        ui.div("Therapeutic Area Breakdown", class_="card-header"),
                        ui.div(
                            ui.output_ui("ta_chart_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(7,
                    ui.div(
                        ui.div("Study Portfolio Overview", class_="card-header"),
                        ui.div(
                            ui.output_ui("portfolio_table_container"),
                            class_="card-body p-0",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Signals Row
            ui.row(
                ui.column(12,
                    ui.div(
                        ui.div("Recent Risk Signals", class_="card-header"),
                        ui.div(
                            ui.output_ui("recent_signals_container"),
                            class_="card-body p-0",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            class_="p-4",
        ),
        icon=ui.tags.i(class_="fa-solid fa-gauge-high"),
    )


def executive_dashboard_server(input, output, session):
    studies = load_studies()
    sites = load_sites()
    kpis = load_kpis()
    signals = load_risk_signals()

    # KPIs
    @render.text
    def kpi_total_studies():
        return str(kpis["total_studies"])

    @render.text
    def kpi_total_enrolled():
        return f"{kpis['total_enrolled']:,}"

    @render.text
    def kpi_enrollment_pct():
        return f"{kpis['overall_enrollment_pct']}%"

    @render.text
    def kpi_active_sites():
        return f"{kpis['total_sites_active']:,}"

    @render.text
    def kpi_open_signals():
        return str(kpis["open_signals"])

    @render.ui
    def kpi_critical_badge():
        n = kpis["critical_signals"]
        if n > 0:
            return ui.span(f"{n} Critical", class_="signal-badge signal-critical")
        return ui.span("None Critical", class_="signal-badge signal-low")

    @render.text
    def kpi_budget_util():
        return f"{kpis['budget_utilization_pct']}%"

    # Enrollment progress chart
    @render.ui
    def enrollment_chart_container():
        fig = go.Figure()

        sorted_studies = studies.sort_values("enrollment_pct", ascending=True)

        # Target bars
        fig.add_trace(go.Bar(
            y=sorted_studies["study_id"],
            x=sorted_studies["target_enrollment"],
            name="Target",
            orientation="h",
            marker_color="#E5E7EB",
            hovertemplate="Target: %{x}<extra></extra>",
        ))

        # Actual bars
        colors = [
            COLORS["risk_high"] if r == "High" else
            COLORS["risk_medium"] if r == "Medium" else
            COLORS["risk_low"]
            for r in sorted_studies["risk_level"]
        ]

        fig.add_trace(go.Bar(
            y=sorted_studies["study_id"],
            x=sorted_studies["current_enrollment"],
            name="Enrolled",
            orientation="h",
            marker_color=colors,
            hovertemplate="Enrolled: %{x} (%{customdata}%)<extra></extra>",
            customdata=sorted_studies["enrollment_pct"],
        ))

        fig.update_layout(
            barmode="overlay",
            height=350,
            margin=dict(t=10, b=30, l=120, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Patients",
            **PLOTLY_TEMPLATE["layout"],
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Risk distribution
    @render.ui
    def risk_dist_container():
        risk_counts = studies["risk_level"].value_counts()
        colors_map = {"Low": COLORS["risk_low"], "Medium": COLORS["risk_medium"], "High": COLORS["risk_high"]}

        fig = go.Figure(data=[go.Pie(
            labels=risk_counts.index.tolist(),
            values=risk_counts.values.tolist(),
            hole=0.55,
            marker_colors=[colors_map.get(r, "#999") for r in risk_counts.index],
            textinfo="label+value",
            textfont_size=12,
            hovertemplate="%{label}: %{value} studies<extra></extra>",
        )])

        fig.update_layout(
            height=350,
            margin=dict(t=10, b=10, l=10, r=10),
            showlegend=False,
            annotations=[dict(text=f"{kpis['avg_risk_score']:.0%}", x=0.5, y=0.55, font_size=24, font_color=COLORS["primary"], font_weight=700, showarrow=False),
                         dict(text="Avg Risk", x=0.5, y=0.42, font_size=11, font_color=COLORS["text_secondary"], showarrow=False)],
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Therapeutic area breakdown
    @render.ui
    def ta_chart_container():
        ta_data = studies.groupby("therapeutic_area").agg(
            n_studies=("study_id", "count"),
            total_enrolled=("current_enrollment", "sum"),
            avg_risk=("risk_score", "mean"),
        ).reset_index()

        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=ta_data["therapeutic_area"],
            y=ta_data["n_studies"],
            name="Studies",
            marker_color=COLORS["chart_1"],
            yaxis="y",
        ))
        fig.add_trace(go.Scatter(
            x=ta_data["therapeutic_area"],
            y=ta_data["avg_risk"],
            name="Avg Risk Score",
            mode="markers+lines",
            marker=dict(size=10, color=COLORS["chart_2"]),
            line=dict(color=COLORS["chart_2"], width=2),
            yaxis="y2",
        ))

        fig.update_layout(
            height=350,
            margin=dict(t=10, b=40, l=40, r=40),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            yaxis=dict(title="Number of Studies", gridcolor="#E5E7EB"),
            yaxis2=dict(title="Avg Risk Score", overlaying="y", side="right", range=[0, 1], gridcolor="rgba(0,0,0,0)"),
            xaxis=dict(tickangle=-15),
            **{k: v for k, v in PLOTLY_TEMPLATE["layout"].items() if k not in ["xaxis", "yaxis", "margin"]},
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Portfolio table
    @render.ui
    def portfolio_table_container():
        cols = ["study_id", "therapeutic_area", "phase", "status",
                "enrollment_pct", "n_sites_active", "risk_level"]
        df = studies[cols].copy()

        def status_badge(s):
            cls_map = {"Enrolling": "status-enrolling", "Active - Not Enrolling": "status-active",
                       "Completed": "status-completed", "Startup": "status-startup"}
            cls = cls_map.get(s, "")
            return f'<span class="status-badge {cls}">{s}</span>'

        def risk_badge(r):
            cls_map = {"Low": "signal-low", "Medium": "signal-medium", "High": "signal-high"}
            cls = cls_map.get(r, "")
            return f'<span class="signal-badge {cls}">{r}</span>'

        df["status"] = df["status"].apply(status_badge)
        df["risk_level"] = df["risk_level"].apply(risk_badge)
        df["enrollment_pct"] = df["enrollment_pct"].apply(lambda x: f"{x}%")

        df.columns = ["Study ID", "Therapeutic Area", "Phase", "Status",
                       "Enrollment %", "Active Sites", "Risk"]

        html = df.to_html(index=False, escape=False, classes="table table-sm table-hover mb-0")
        return ui.HTML(f'<div class="table-container" style="max-height: 350px; overflow-y: auto;">{html}</div>')

    # Recent signals
    @render.ui
    def recent_signals_container():
        recent = signals.sort_values("detected_date", ascending=False).head(8)
        cols = ["signal_id", "study_id", "signal_name", "severity", "status",
                "detected_date", "assigned_to"]
        df = recent[cols].copy()

        def severity_badge(s):
            cls_map = {"Critical": "signal-critical", "High": "signal-high",
                       "Medium": "signal-medium", "Low": "signal-low"}
            return f'<span class="signal-badge {cls_map.get(s, "")}">{s}</span>'

        df["severity"] = df["severity"].apply(severity_badge)
        df["detected_date"] = pd.to_datetime(df["detected_date"]).dt.strftime("%Y-%m-%d")

        df.columns = ["Signal ID", "Study", "Signal", "Severity", "Status",
                       "Detected", "Assigned To"]

        html = df.to_html(index=False, escape=False, classes="table table-sm table-hover mb-0")
        return ui.HTML(f'<div class="table-container">{html}</div>')
