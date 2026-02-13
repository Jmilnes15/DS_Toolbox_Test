"""
Clinical Control Tower - Simulated Trial Data Generator
========================================================
Generates realistic clinical trial operational data for the Control Tower demo.
Simulates a portfolio of oncology, neurology, and rare disease trials across
global sites with enrollment, quality, supply, and financial metrics.

This script would normally run as a scheduled Quarto job on Posit Connect,
pulling from CTMS, EDC, and other source systems. For this demo, we simulate
the data to showcase the full pipeline.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import json
import os

np.random.seed(42)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------
OUTPUT_DIR = os.path.join(os.path.dirname(__file__))

THERAPEUTIC_AREAS = ["Oncology", "Neurology", "Rare Disease", "Immunology", "Cardiovascular"]
PHASES = ["Phase I", "Phase II", "Phase III", "Phase IV"]
STATUSES = ["Enrolling", "Active - Not Enrolling", "Completed", "Startup"]

COUNTRIES = {
    "United States": {"region": "North America", "lat": 39.8, "lon": -98.5, "sites_weight": 3.0},
    "Canada": {"region": "North America", "lat": 56.1, "lon": -106.3, "sites_weight": 1.0},
    "United Kingdom": {"region": "Europe", "lat": 55.3, "lon": -3.4, "sites_weight": 1.5},
    "Germany": {"region": "Europe", "lat": 51.1, "lon": 10.4, "sites_weight": 1.8},
    "France": {"region": "Europe", "lat": 46.2, "lon": 2.2, "sites_weight": 1.5},
    "Spain": {"region": "Europe", "lat": 40.4, "lon": -3.7, "sites_weight": 1.2},
    "Italy": {"region": "Europe", "lat": 41.9, "lon": 12.5, "sites_weight": 1.2},
    "Poland": {"region": "Europe", "lat": 51.9, "lon": 19.1, "sites_weight": 1.0},
    "Japan": {"region": "Asia-Pacific", "lat": 36.2, "lon": 138.2, "sites_weight": 1.5},
    "South Korea": {"region": "Asia-Pacific", "lat": 35.9, "lon": 127.7, "sites_weight": 1.0},
    "Australia": {"region": "Asia-Pacific", "lat": -25.3, "lon": 133.8, "sites_weight": 0.8},
    "India": {"region": "Asia-Pacific", "lat": 20.6, "lon": 78.9, "sites_weight": 1.5},
    "Brazil": {"region": "Latin America", "lat": -14.2, "lon": -51.9, "sites_weight": 1.2},
    "Argentina": {"region": "Latin America", "lat": -38.4, "lon": -63.6, "sites_weight": 0.8},
    "South Africa": {"region": "Africa", "lat": -30.6, "lon": 22.9, "sites_weight": 0.6},
}

SITE_NAMES = [
    "Memorial Cancer Center", "University Medical Center", "General Hospital",
    "Regional Research Institute", "Academic Health System", "Clinical Research Center",
    "Metropolitan Hospital", "National Medical Center", "Community Health Network",
    "Translational Research Hospital", "Center for Advanced Medicine",
    "Institute of Clinical Sciences", "Health Sciences Center", "Medical Research Clinic",
    "Comprehensive Care Center", "Teaching Hospital", "Biomedical Research Institute",
]

INVESTIGATORS = [
    "Dr. Chen", "Dr. Patel", "Dr. Mueller", "Dr. Tanaka", "Dr. Silva",
    "Dr. Johnson", "Dr. Kim", "Dr. Garcia", "Dr. Williams", "Dr. Brown",
    "Dr. Nakamura", "Dr. Schmidt", "Dr. Lopez", "Dr. Anderson", "Dr. Taylor",
    "Dr. Yamamoto", "Dr. Fischer", "Dr. Martinez", "Dr. Thompson", "Dr. Lee",
    "Dr. Petrov", "Dr. Rossi", "Dr. Dubois", "Dr. Singh", "Dr. O'Brien",
]


def generate_studies(n_studies=12):
    """Generate a portfolio of clinical studies."""
    studies = []
    compounds = [f"BIO-{np.random.randint(1000,9999)}" for _ in range(n_studies)]

    for i in range(n_studies):
        ta = np.random.choice(THERAPEUTIC_AREAS, p=[0.30, 0.25, 0.15, 0.20, 0.10])
        phase = np.random.choice(PHASES, p=[0.15, 0.30, 0.35, 0.20])
        status = np.random.choice(STATUSES, p=[0.45, 0.25, 0.20, 0.10])

        if phase == "Phase I":
            target_n = np.random.randint(20, 80)
            n_sites = np.random.randint(3, 10)
        elif phase == "Phase II":
            target_n = np.random.randint(80, 300)
            n_sites = np.random.randint(15, 50)
        elif phase == "Phase III":
            target_n = np.random.randint(300, 2000)
            n_sites = np.random.randint(50, 200)
        else:
            target_n = np.random.randint(500, 5000)
            n_sites = np.random.randint(30, 150)

        start_date = datetime(2023, 1, 1) + timedelta(days=np.random.randint(0, 600))
        planned_end = start_date + timedelta(days=np.random.randint(365, 1095))

        if status == "Completed":
            pct_enrolled = 1.0
        elif status == "Enrolling":
            pct_enrolled = np.random.uniform(0.15, 0.85)
        elif status == "Active - Not Enrolling":
            pct_enrolled = 1.0
        else:
            pct_enrolled = 0.0

        current_enrolled = int(target_n * pct_enrolled)

        # Risk score: composite metric
        risk_score = np.clip(np.random.normal(0.4, 0.2), 0.05, 0.95)
        if status == "Enrolling" and pct_enrolled < 0.3:
            risk_score = np.clip(risk_score + 0.2, 0, 0.95)

        studies.append({
            "study_id": f"BIO-{2024+i:04d}-{np.random.randint(100,999)}",
            "compound": compounds[i],
            "study_name": f"{ta} {'Pivotal' if phase=='Phase III' else 'Exploratory'} Study {i+1}",
            "therapeutic_area": ta,
            "phase": phase,
            "status": status,
            "target_enrollment": target_n,
            "current_enrollment": current_enrolled,
            "enrollment_pct": round(pct_enrolled * 100, 1),
            "n_sites_planned": n_sites,
            "n_sites_active": int(n_sites * np.random.uniform(0.6, 1.0)),
            "n_countries": np.random.randint(3, 15),
            "start_date": start_date.strftime("%Y-%m-%d"),
            "planned_end_date": planned_end.strftime("%Y-%m-%d"),
            "risk_score": round(risk_score, 3),
            "risk_level": "High" if risk_score > 0.65 else ("Medium" if risk_score > 0.4 else "Low"),
            "budget_mm": round(np.random.uniform(5, 150), 1),
            "spend_to_date_mm": round(np.random.uniform(1, 100), 1),
            "protocol_amendments": np.random.randint(0, 5),
            "sponsor": "Biogen (Simulated)",
        })

    return pd.DataFrame(studies)


def generate_sites(studies_df):
    """Generate site-level data for each study."""
    all_sites = []
    site_id_counter = 1000

    for _, study in studies_df.iterrows():
        n_sites = study["n_sites_active"]
        countries_for_study = np.random.choice(
            list(COUNTRIES.keys()),
            size=min(study["n_countries"], len(COUNTRIES)),
            replace=False,
            p=[v["sites_weight"] for v in COUNTRIES.values()] / np.sum([v["sites_weight"] for v in COUNTRIES.values()])
        )

        for j in range(n_sites):
            site_id_counter += 1
            country = np.random.choice(countries_for_study)
            info = COUNTRIES[country]

            # Simulate site performance
            screen_rate = max(0, np.random.normal(2.5, 1.5))  # patients/month
            screen_fail_pct = np.clip(np.random.normal(0.25, 0.1), 0.05, 0.60)
            enroll_rate = screen_rate * (1 - screen_fail_pct)

            quality_score = np.clip(np.random.normal(0.75, 0.15), 0.3, 1.0)
            query_rate = max(0, np.random.normal(5, 3))  # queries per 100 CRFs

            # Site activation timeline
            days_to_activate = max(30, int(np.random.normal(90, 30)))
            activation_date = datetime.strptime(study["start_date"], "%Y-%m-%d") + timedelta(days=days_to_activate)

            site_enrolled = max(0, int(np.random.poisson(enroll_rate * 6)))

            # Protocol deviations
            n_deviations = np.random.poisson(1.5)
            major_deviations = np.random.poisson(0.3)

            all_sites.append({
                "study_id": study["study_id"],
                "site_id": f"SITE-{site_id_counter}",
                "site_name": f"{np.random.choice(SITE_NAMES)} - {country}",
                "investigator": np.random.choice(INVESTIGATORS),
                "country": country,
                "region": info["region"],
                "lat": info["lat"] + np.random.uniform(-3, 3),
                "lon": info["lon"] + np.random.uniform(-3, 3),
                "status": np.random.choice(
                    ["Active", "Active", "Active", "Pending", "Closed"],
                    p=[0.6, 0.15, 0.1, 0.1, 0.05]
                ),
                "activation_date": activation_date.strftime("%Y-%m-%d"),
                "days_to_activate": days_to_activate,
                "patients_screened": int(site_enrolled / max(0.01, (1 - screen_fail_pct))),
                "patients_enrolled": site_enrolled,
                "screen_fail_rate": round(screen_fail_pct * 100, 1),
                "enrollment_rate_per_month": round(enroll_rate, 2),
                "target_enrollment": max(1, int(study["target_enrollment"] / n_sites * np.random.uniform(0.5, 1.5))),
                "quality_score": round(quality_score, 3),
                "query_rate_per_100_crfs": round(query_rate, 1),
                "protocol_deviations": n_deviations,
                "major_deviations": major_deviations,
                "monitoring_visits_completed": np.random.randint(1, 12),
                "monitoring_visits_planned": np.random.randint(6, 18),
                "last_monitoring_visit": (datetime.now() - timedelta(days=np.random.randint(1, 60))).strftime("%Y-%m-%d"),
            })

    return pd.DataFrame(all_sites)


def generate_enrollment_timeseries(studies_df, sites_df):
    """Generate weekly enrollment timeseries for forecasting."""
    all_ts = []

    for _, study in studies_df.iterrows():
        start = datetime.strptime(study["start_date"], "%Y-%m-%d")
        weeks = max(10, (datetime.now() - start).days // 7)

        study_sites = sites_df[sites_df["study_id"] == study["study_id"]]
        base_rate = study_sites["enrollment_rate_per_month"].mean() * len(study_sites) / 4.33

        # S-curve enrollment with noise
        target = study["target_enrollment"]
        cumulative = 0
        planned_cumulative = 0

        for w in range(min(weeks, 104)):
            week_date = start + timedelta(weeks=w)

            # Actual enrollment (S-curve with seasonal variation + noise)
            t_norm = w / max(1, weeks)
            s_curve = 1 / (1 + np.exp(-8 * (t_norm - 0.4)))
            seasonal = 1 + 0.15 * np.sin(2 * np.pi * w / 52)
            weekly_actual = max(0, int(base_rate * s_curve * seasonal * np.random.uniform(0.5, 1.8)))
            cumulative = min(target, cumulative + weekly_actual)

            # Planned enrollment (linear)
            planned_weekly = target / max(1, weeks)
            planned_cumulative = min(target, planned_cumulative + planned_weekly)

            all_ts.append({
                "study_id": study["study_id"],
                "week": w + 1,
                "date": week_date.strftime("%Y-%m-%d"),
                "weekly_enrolled": weekly_actual,
                "cumulative_enrolled": cumulative,
                "planned_cumulative": round(planned_cumulative),
                "target_enrollment": target,
                "enrollment_gap": round(planned_cumulative - cumulative),
            })

    return pd.DataFrame(all_ts)


def generate_risk_signals(studies_df, sites_df):
    """Generate risk signals and alerts for the control tower."""
    signals = []
    signal_types = [
        ("Enrollment Below Target", "enrollment", "Enrollment rate is significantly below planned trajectory"),
        ("High Screen Failure Rate", "quality", "Screen failure rate exceeds protocol threshold"),
        ("Data Quality Alert", "quality", "Query rate per 100 CRFs exceeds acceptable threshold"),
        ("Protocol Deviation Trend", "compliance", "Increasing trend in protocol deviations detected"),
        ("Site Activation Delay", "operational", "Site activation exceeding planned timeline"),
        ("Supply Chain Risk", "supply", "Drug supply levels approaching minimum threshold"),
        ("Monitoring Visit Overdue", "compliance", "Scheduled monitoring visit is overdue by >30 days"),
        ("Competitive Recruitment Risk", "strategic", "Competing trial opened at site catchment area"),
        ("Regulatory Milestone At Risk", "regulatory", "Upcoming regulatory deadline with incomplete data"),
        ("Budget Variance Alert", "financial", "Study spending deviating >15% from forecast"),
    ]

    for _, study in studies_df.iterrows():
        study_sites = sites_df[sites_df["study_id"] == study["study_id"]]

        # Generate 2-6 signals per study
        n_signals = np.random.randint(2, 7)
        chosen = np.random.choice(len(signal_types), size=n_signals, replace=False)

        for idx in chosen:
            sig_name, sig_category, sig_desc = signal_types[idx]
            severity = np.random.choice(["Critical", "High", "Medium", "Low"], p=[0.1, 0.25, 0.40, 0.25])

            affected_sites = []
            if len(study_sites) > 0:
                n_affected = np.random.randint(1, min(6, len(study_sites) + 1))
                affected_sites = study_sites.sample(n=n_affected)["site_id"].tolist()

            detected_date = datetime.now() - timedelta(days=np.random.randint(0, 30))

            signals.append({
                "signal_id": f"SIG-{np.random.randint(10000, 99999)}",
                "study_id": study["study_id"],
                "signal_name": sig_name,
                "category": sig_category,
                "description": sig_desc,
                "severity": severity,
                "status": np.random.choice(["Open", "Under Review", "Mitigated", "Closed"], p=[0.35, 0.30, 0.20, 0.15]),
                "detected_date": detected_date.strftime("%Y-%m-%d"),
                "affected_sites": json.dumps(affected_sites),
                "n_affected_sites": len(affected_sites),
                "impact_score": round(np.random.uniform(0.1, 1.0), 2),
                "recommended_action": np.random.choice([
                    "Increase monitoring frequency",
                    "Conduct root cause analysis",
                    "Escalate to study lead",
                    "Implement corrective action plan",
                    "Schedule ad-hoc site visit",
                    "Review with medical monitor",
                    "Adjust enrollment targets",
                    "Engage backup sites",
                ]),
                "assigned_to": np.random.choice([
                    "Clinical Operations Lead",
                    "Medical Monitor",
                    "Data Management Lead",
                    "Study Director",
                    "Regional CRA Lead",
                    "Supply Chain Manager",
                ]),
                "days_open": np.random.randint(0, 45),
            })

    return pd.DataFrame(signals)


def generate_kpi_summary(studies_df, sites_df, signals_df):
    """Generate portfolio-level KPI summary."""
    enrolling = studies_df[studies_df["status"] == "Enrolling"]

    kpis = {
        "total_studies": len(studies_df),
        "enrolling_studies": len(enrolling),
        "total_sites_active": int(studies_df["n_sites_active"].sum()),
        "total_countries": int(studies_df["n_countries"].sum()),
        "total_enrolled": int(studies_df["current_enrollment"].sum()),
        "total_target": int(studies_df["target_enrollment"].sum()),
        "overall_enrollment_pct": round(
            studies_df["current_enrollment"].sum() / max(1, studies_df["target_enrollment"].sum()) * 100, 1
        ),
        "avg_risk_score": round(studies_df["risk_score"].mean(), 3),
        "high_risk_studies": int((studies_df["risk_level"] == "High").sum()),
        "open_signals": int((signals_df["status"].isin(["Open", "Under Review"])).sum()),
        "critical_signals": int(
            ((signals_df["severity"] == "Critical") & (signals_df["status"].isin(["Open", "Under Review"]))).sum()
        ),
        "avg_site_quality": round(sites_df["quality_score"].mean(), 3),
        "total_budget_mm": round(studies_df["budget_mm"].sum(), 1),
        "total_spend_mm": round(studies_df["spend_to_date_mm"].sum(), 1),
        "budget_utilization_pct": round(
            studies_df["spend_to_date_mm"].sum() / max(1, studies_df["budget_mm"].sum()) * 100, 1
        ),
        "generated_at": datetime.now().isoformat(),
    }
    return kpis


def main():
    """Generate all datasets and save to CSV."""
    print("Generating Clinical Control Tower data...")

    studies_df = generate_studies(n_studies=12)
    print(f"  Generated {len(studies_df)} studies")

    sites_df = generate_sites(studies_df)
    print(f"  Generated {len(sites_df)} site records")

    enrollment_ts = generate_enrollment_timeseries(studies_df, sites_df)
    print(f"  Generated {len(enrollment_ts)} enrollment timeseries records")

    signals_df = generate_risk_signals(studies_df, sites_df)
    print(f"  Generated {len(signals_df)} risk signals")

    kpis = generate_kpi_summary(studies_df, sites_df, signals_df)
    print(f"  Generated portfolio KPIs")

    # Save all data
    studies_df.to_csv(os.path.join(OUTPUT_DIR, "studies.csv"), index=False)
    sites_df.to_csv(os.path.join(OUTPUT_DIR, "sites.csv"), index=False)
    enrollment_ts.to_csv(os.path.join(OUTPUT_DIR, "enrollment_timeseries.csv"), index=False)
    signals_df.to_csv(os.path.join(OUTPUT_DIR, "risk_signals.csv"), index=False)

    with open(os.path.join(OUTPUT_DIR, "kpi_summary.json"), "w") as f:
        json.dump(kpis, f, indent=2)

    print("All data saved successfully.")
    return studies_df, sites_df, enrollment_ts, signals_df, kpis


if __name__ == "__main__":
    main()
