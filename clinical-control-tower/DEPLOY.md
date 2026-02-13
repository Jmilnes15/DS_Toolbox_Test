# Clinical Control Tower - Deployment Guide

## Quick Deploy to Posit Connect

### Prerequisites
- Python 3.9+
- A Posit Connect server
- `rsconnect-python` installed: `pip install rsconnect-python`

### Step 1: Generate Data & Train Models

```bash
cd clinical-control-tower

# Install dependencies
pip install -r requirements.txt

# Generate simulated trial data
python data/generate_trial_data.py

# Train ML models
python models/train_models.py
```

### Step 2: Test Locally

```bash
cd app
shiny run app.py --port 8080
```

### Step 3: Deploy to Posit Connect

```bash
# Configure your Connect server (one-time setup)
rsconnect add \
  --server https://your-connect-server.com \
  --name my-connect \
  --api-key YOUR_API_KEY

# Deploy the Shiny app
rsconnect deploy shiny \
  --server my-connect \
  --title "Clinical Control Tower" \
  ./app/
```

### Step 4: Deploy Supporting Artifacts

```bash
# Deploy the ETL pipeline report (for scheduled execution)
rsconnect deploy quarto \
  --server my-connect \
  --title "Control Tower ETL Pipeline" \
  ./quarto/etl_pipeline_report.qmd
```

## Project Structure

```
clinical-control-tower/
├── app/                          # Shiny for Python application
│   ├── app.py                    # Main application entry point
│   ├── requirements.txt          # App dependencies
│   ├── modules/                  # Page modules
│   │   ├── executive_dashboard.py
│   │   ├── enrollment_forecasting.py
│   │   ├── site_performance.py
│   │   ├── risk_signals.py
│   │   └── how_it_works.py
│   └── utils/                    # Shared utilities
│       ├── data_loader.py        # Data loading functions
│       └── theme.py              # Styling and theme constants
├── data/                         # Data layer
│   ├── generate_trial_data.py    # Data generation script
│   ├── studies.csv               # Study-level data
│   ├── sites.csv                 # Site-level data
│   ├── enrollment_timeseries.csv # Weekly enrollment data
│   ├── risk_signals.csv          # Risk signal data
│   ├── site_rankings.csv         # Computed site rankings
│   └── kpi_summary.json          # Portfolio KPIs
├── models/                       # ML model artifacts
│   ├── train_models.py           # Model training pipeline
│   ├── enrollment_forecaster.pkl # Enrollment prediction model
│   └── risk_classifier.pkl       # Site risk classifier
├── quarto/                       # Quarto reports
│   └── etl_pipeline_report.qmd   # ETL pipeline documentation
├── requirements.txt              # Project-wide dependencies
└── DEPLOY.md                     # This file
```

## Architecture

This demo showcases the full Posit ecosystem:

| Component | Tool | Role |
|-----------|------|------|
| Development | **Posit Workbench** | Governed IDE environment |
| ETL Pipeline | **Quarto + Connect** | Scheduled data refresh |
| Data Versioning | **Pins** | Versioned data artifacts |
| ML Models | **scikit-learn + Vetiver** | Training & deployment |
| Model APIs | **Vetiver + Connect** | REST API hosting |
| Dashboard | **Shiny for Python** | Interactive application |
| Deployment | **Posit Connect** | Hosting, auth, scaling |
| Packages | **Posit Package Manager** | Validated repositories |
