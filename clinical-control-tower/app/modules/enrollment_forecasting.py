"""
Enrollment Forecasting Module
================================
AI-powered enrollment predictions with interactive study selection,
forecast visualization, and scenario analysis.
"""

from shiny import ui, render, reactive
import plotly.graph_objects as go
import pandas as pd
import numpy as np

from utils.data_loader import (
    load_studies, load_enrollment_ts, forecast_enrollment,
    load_enrollment_model_metrics,
)
from utils.theme import COLORS, PLOTLY_TEMPLATE


def enrollment_forecasting_ui():
    studies = load_studies()
    enrolling = studies[studies["status"].isin(["Enrolling", "Active - Not Enrolling"])]
    study_choices = {row["study_id"]: f"{row['study_id']} - {row['study_name']}"
                     for _, row in enrolling.iterrows()}

    return ui.nav_panel(
        "Enrollment Forecasting",
        ui.div(
            # Header
            ui.div(
                ui.h4("AI-Powered Enrollment Forecasting", class_="section-header"),
                ui.p("Select a study to view historical enrollment and ML-driven forecasts. "
                     "The model uses gradient boosting to predict weekly enrollment rates based on "
                     "historical patterns, seasonality, and enrollment velocity.",
                     style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem;"),
            ),

            # Posit callout
            ui.div(
                ui.div("Posit Connect + Vetiver", class_="callout-title"),
                ui.div("In production, the enrollment forecasting model is trained in Posit Workbench, "
                       "versioned with Vetiver, stored via Pins, and served as a real-time API on "
                       "Posit Connect. When new data arrives, the Quarto ETL pipeline triggers a model "
                       "refresh — all without leaving the Posit ecosystem.",
                       class_="callout-body"),
                class_="posit-callout mb-4",
            ),

            # Controls
            ui.row(
                ui.column(5,
                    ui.div(
                        ui.row(
                            ui.column(8,
                                ui.input_select("forecast_study", "Select Study",
                                                choices=study_choices,
                                                width="100%"),
                            ),
                            ui.column(4,
                                ui.input_slider("forecast_weeks", "Forecast Weeks",
                                                min=4, max=26, value=12, step=2),
                            ),
                        ),
                        class_="filter-panel",
                    ),
                ),
                ui.column(7,
                    ui.row(
                        ui.column(3,
                            ui.div(
                                ui.div(
                                    ui.div(ui.output_text("fc_current_enrolled"), class_="value"),
                                    ui.div("Currently Enrolled", class_="label"),
                                    class_="kpi-metric",
                                ),
                                class_="card",
                            ),
                        ),
                        ui.column(3,
                            ui.div(
                                ui.div(
                                    ui.div(ui.output_text("fc_target"), class_="value"),
                                    ui.div("Target Enrollment", class_="label"),
                                    class_="kpi-metric",
                                ),
                                class_="card",
                            ),
                        ),
                        ui.column(3,
                            ui.div(
                                ui.div(
                                    ui.div(ui.output_text("fc_predicted_date"), class_="value"),
                                    ui.div("Est. Target Date", class_="label"),
                                    class_="kpi-metric",
                                ),
                                class_="card",
                            ),
                        ),
                        ui.column(3,
                            ui.div(
                                ui.div(
                                    ui.div(ui.output_text("fc_weekly_rate"), class_="value"),
                                    ui.div("Avg Weekly Rate", class_="label"),
                                    class_="kpi-metric",
                                ),
                                class_="card",
                            ),
                        ),
                        class_="g-3",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Main forecast chart
            ui.row(
                ui.column(12,
                    ui.div(
                        ui.div("Enrollment Trajectory & Forecast", class_="card-header"),
                        ui.div(
                            ui.output_ui("forecast_chart_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            # Details row
            ui.row(
                ui.column(6,
                    ui.div(
                        ui.div("Weekly Enrollment Rate", class_="card-header"),
                        ui.div(
                            ui.output_ui("weekly_rate_chart_container"),
                            class_="card-body p-2",
                        ),
                        class_="card",
                    ),
                ),
                ui.column(6,
                    ui.div(
                        ui.div("Model Performance", class_="card-header"),
                        ui.div(
                            ui.output_ui("model_info_container"),
                            class_="card-body p-3",
                        ),
                        class_="card",
                    ),
                ),
                class_="mb-4 g-3",
            ),

            class_="p-4",
        ),
        icon=ui.tags.i(class_="fa-solid fa-chart-line"),
    )


def enrollment_forecasting_server(input, output, session):
    studies = load_studies()
    enrollment_ts = load_enrollment_ts()
    model_metrics = load_enrollment_model_metrics()

    @reactive.calc
    def selected_study_data():
        study_id = input.forecast_study()
        study = studies[studies["study_id"] == study_id].iloc[0]
        ts = enrollment_ts[enrollment_ts["study_id"] == study_id].sort_values("week")
        forecast = forecast_enrollment(study_id, weeks_ahead=input.forecast_weeks())
        return study, ts, forecast

    # KPIs
    @render.text
    def fc_current_enrolled():
        study, ts, _ = selected_study_data()
        return f"{study['current_enrollment']:,}"

    @render.text
    def fc_target():
        study, _, _ = selected_study_data()
        return f"{study['target_enrollment']:,}"

    @render.text
    def fc_predicted_date():
        _, _, forecast = selected_study_data()
        if len(forecast) > 0:
            target = forecast["target_enrollment"].iloc[0]
            reached = forecast[forecast["cumulative_forecast"] >= target * 0.95]
            if len(reached) > 0:
                return reached.iloc[0]["date"].strftime("%b %Y")
        return "TBD"

    @render.text
    def fc_weekly_rate():
        _, ts, _ = selected_study_data()
        if len(ts) > 4:
            recent = ts.tail(8)["weekly_enrolled"].mean()
            return f"{recent:.1f}"
        return "N/A"

    # Main forecast chart
    @render.ui
    def forecast_chart_container():
        study, ts, forecast = selected_study_data()

        fig = go.Figure()

        # Planned line
        fig.add_trace(go.Scatter(
            x=ts["date"], y=ts["planned_cumulative"],
            name="Planned",
            line=dict(color="#B0BEC5", width=2, dash="dash"),
            hovertemplate="Planned: %{y:,.0f}<extra></extra>",
        ))

        # Actual enrollment
        fig.add_trace(go.Scatter(
            x=ts["date"], y=ts["cumulative_enrolled"],
            name="Actual Enrolled",
            line=dict(color=COLORS["chart_1"], width=3),
            fill="tozeroy",
            fillcolor="rgba(46, 134, 171, 0.08)",
            hovertemplate="Actual: %{y:,.0f}<extra></extra>",
        ))

        # Forecast
        if len(forecast) > 0:
            # Connect forecast to last actual point
            last_actual = ts.iloc[-1]
            forecast_dates = pd.concat([
                pd.DataFrame([{"date": last_actual["date"], "cumulative_forecast": last_actual["cumulative_enrolled"]}]),
                forecast[["date", "cumulative_forecast"]],
            ])

            fig.add_trace(go.Scatter(
                x=forecast_dates["date"],
                y=forecast_dates["cumulative_forecast"],
                name="ML Forecast",
                line=dict(color=COLORS["accent"], width=3, dash="dot"),
                hovertemplate="Forecast: %{y:,.0f}<extra></extra>",
            ))

            # Confidence band
            upper = forecast["cumulative_forecast"] * 1.15
            lower = forecast["cumulative_forecast"] * 0.85
            fig.add_trace(go.Scatter(
                x=pd.concat([forecast["date"], forecast["date"][::-1]]),
                y=pd.concat([upper, lower[::-1]]),
                fill="toself",
                fillcolor="rgba(162, 59, 114, 0.1)",
                line=dict(color="rgba(0,0,0,0)"),
                name="Confidence Band",
                showlegend=True,
                hoverinfo="skip",
            ))

        # Target line
        fig.add_hline(y=study["target_enrollment"],
                      line_dash="dot", line_color=COLORS["success"],
                      annotation_text=f"Target: {study['target_enrollment']:,}",
                      annotation_position="top right",
                      annotation_font_color=COLORS["success"])

        fig.update_layout(
            height=400,
            margin=dict(t=20, b=40, l=60, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Date",
            yaxis_title="Cumulative Patients Enrolled",
            **PLOTLY_TEMPLATE["layout"],
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Weekly rate chart
    @render.ui
    def weekly_rate_chart_container():
        _, ts, _ = selected_study_data()

        # Moving average
        ts_copy = ts.copy()
        ts_copy["ma_4wk"] = ts_copy["weekly_enrolled"].rolling(window=4, min_periods=1).mean()

        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=ts_copy["date"], y=ts_copy["weekly_enrolled"],
            name="Weekly Enrolled",
            marker_color=COLORS["chart_1"],
            opacity=0.4,
            hovertemplate="Week: %{y}<extra></extra>",
        ))

        fig.add_trace(go.Scatter(
            x=ts_copy["date"], y=ts_copy["ma_4wk"],
            name="4-Week Moving Avg",
            line=dict(color=COLORS["accent"], width=2.5),
            hovertemplate="4-wk avg: %{y:.1f}<extra></extra>",
        ))

        fig.update_layout(
            height=300,
            margin=dict(t=10, b=40, l=50, r=20),
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
            xaxis_title="Date",
            yaxis_title="Patients / Week",
            **PLOTLY_TEMPLATE["layout"],
        )

        return ui.HTML(fig.to_html(full_html=False, include_plotlyjs="cdn", config={"displayModeBar": False}))

    # Model info
    @render.ui
    def model_info_container():
        metrics = model_metrics

        items = [
            ("Model Type", metrics.get("model_type", "N/A")),
            ("Cross-Val R\u00b2", f"{metrics.get('r2_mean', 0):.4f} \u00b1 {metrics.get('r2_std', 0):.4f}"),
            ("Training Samples", f"{metrics.get('n_samples', 0):,}"),
            ("Features Used", str(len(metrics.get("features", [])))),
            ("Last Trained", metrics.get("trained_at", "N/A")[:10]),
        ]

        rows = ""
        for label, value in items:
            rows += f"""
            <tr>
                <td style="font-weight: 600; color: var(--text-secondary); width: 45%;">{label}</td>
                <td style="font-weight: 500;">{value}</td>
            </tr>
            """

        features_html = ""
        for f in metrics.get("features", []):
            features_html += f'<span class="signal-badge signal-low" style="margin: 2px;">{f}</span> '

        html = f"""
        <table class="table table-sm mb-3" style="font-size: 0.9rem;">
            <tbody>{rows}</tbody>
        </table>
        <div style="margin-top: 0.75rem;">
            <div style="font-weight: 600; font-size: 0.8rem; color: var(--text-secondary);
                        text-transform: uppercase; margin-bottom: 0.5rem;">Features</div>
            {features_html}
        </div>
        <div class="posit-callout" style="margin-top: 1rem;">
            <div class="callout-title">Vetiver Model Card</div>
            <div class="callout-body">In production, this model would have a full Vetiver model card
            with performance metrics, fairness checks, and deployment metadata — all versioned on
            Posit Connect.</div>
        </div>
        """

        return ui.HTML(html)
