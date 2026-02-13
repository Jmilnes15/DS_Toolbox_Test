# AI Agent Deployment Instructions: Clinical Control Tower to Posit Connect

## Purpose

You are deploying the Clinical Control Tower Shiny for Python application to
a Posit Connect server. Follow these instructions exactly and in order.

---

## Prerequisites — Verify Before Starting

1. **Python 3.9+** must be installed.
2. **`rsconnect-python`** must be installed (`pip install rsconnect-python`).
3. You must have a **Posit Connect server URL** and a valid **API key** with
   publisher permissions. The user should provide these or they should be
   available as environment variables (`CONNECT_SERVER` and `CONNECT_API_KEY`).
4. The working directory should be the root of this repository, with the
   `clinical-control-tower/` folder present.

---

## Step 1: Understand the Bundling Requirement

**CRITICAL:** Posit Connect deploys the `app/` directory as a self-contained
bundle. The Shiny app entry point is `app/app.py`. However, the app loads data
files from `data/` and model files from `models/`, which are **sibling
directories** outside `app/`.

The data loader at `app/utils/data_loader.py` resolves paths relative to the
file's location:

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
```

This means `BASE_DIR` points to `clinical-control-tower/`, and expects `data/`
and `models/` to exist at that level. When deploying to Connect, you have
**two options** (choose one):

### Option A: Deploy the entire `clinical-control-tower/` directory (Recommended)

Deploy from the parent of `app/` so that `data/` and `models/` are included
in the bundle. Use the `--entrypoint` flag to tell Connect which file is the
app entry point.

```bash
cd clinical-control-tower
rsconnect deploy shiny . \
  --entrypoint app/app.py \
  --title "Clinical Control Tower" \
  --server YOUR_SERVER_NAME
```

### Option B: Copy data into app/ and adjust paths

If Option A does not work with your version of rsconnect-python, copy the
data and model directories into `app/` and update the data loader:

```bash
cp -r data/ app/data/
cp -r models/ app/models/
```

Then edit `app/utils/data_loader.py` and change lines 13-14 to:

```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
MODEL_DIR = os.path.join(BASE_DIR, "models")
```

(Change from 3 levels of `dirname` to 2, since data/ and models/ are now
inside app/ rather than one level above it.)

Then deploy:

```bash
rsconnect deploy shiny app/ \
  --title "Clinical Control Tower" \
  --server YOUR_SERVER_NAME
```

---

## Step 2: Regenerate Data (If Needed)

If the CSV files in `data/` are missing or you want fresh data:

```bash
cd clinical-control-tower
pip install -r requirements.txt
python data/generate_trial_data.py
python models/train_models.py
```

This generates:
- `data/studies.csv` — 12 clinical trials
- `data/sites.csv` — ~600 trial sites
- `data/enrollment_timeseries.csv` — weekly enrollment data
- `data/risk_signals.csv` — risk alerts
- `data/site_rankings.csv` — computed site rankings
- `data/kpi_summary.json` — portfolio KPIs
- `models/enrollment_forecaster.pkl` — trained ML model
- `models/risk_classifier.pkl` — trained ML model
- `models/*.json` — model metrics

**Verify all files exist before deploying.**

---

## Step 3: Configure the Connect Server

If a server has not been configured yet in rsconnect-python:

```bash
rsconnect add \
  --server https://YOUR_CONNECT_URL \
  --name my-connect \
  --api-key YOUR_API_KEY
```

Replace `YOUR_CONNECT_URL` with the actual Posit Connect server URL
(e.g., `https://connect.company.com`) and `YOUR_API_KEY` with a valid API key.

To verify the configuration:

```bash
rsconnect list
```

The server should appear in the output.

---

## Step 4: Deploy the Shiny Application

Run the deploy command. Use the server name you configured in Step 3.

**Option A (recommended):**

```bash
cd clinical-control-tower
rsconnect deploy shiny . \
  --entrypoint app/app.py \
  --title "Clinical Control Tower" \
  --server my-connect
```

**Option B (if Option A fails):**

```bash
cd clinical-control-tower
cp -r data/ app/data/
cp -r models/ app/models/
```

Edit `app/utils/data_loader.py` line 13 — change:
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
```
to:
```python
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
```

Then deploy:
```bash
rsconnect deploy shiny app/ \
  --title "Clinical Control Tower" \
  --server my-connect
```

---

## Step 5: Verify the Deployment

1. The deploy command will print a **content URL** on success. Open it in a
   browser.
2. Verify all 5 tabs load correctly:
   - **Executive Dashboard** — KPI cards, enrollment progress chart, risk donut
   - **Enrollment Forecasting** — Study selector, forecast line chart with
     confidence band
   - **Site Performance** — Site ranking bars, geographic map, radar chart
   - **Risk Signals** — Heatmap, funnel, impact bubble chart
   - **How This Works** — Full workflow architecture page
3. If the app shows errors, check the Connect logs for the deployment. Common
   issues:
   - **"FileNotFoundError: studies.csv"** — Data files were not included in the
     bundle. Use Option B above.
   - **"ModuleNotFoundError"** — A dependency is missing from `requirements.txt`.
     Add it and redeploy.
   - **Timeout on startup** — The app loads data at startup. Increase the
     startup timeout in Connect settings for this content if needed.

---

## Step 6: (Optional) Deploy the ETL Pipeline Report

The Quarto ETL report can be deployed separately and scheduled:

```bash
rsconnect deploy quarto quarto/etl_pipeline_report.qmd \
  --title "Control Tower ETL Pipeline" \
  --server my-connect
```

After deployment, configure a schedule in the Connect UI (e.g., daily at 6 AM)
to simulate an automated data refresh pipeline.

---

## Step 7: (Optional) Configure Access Controls

In the Posit Connect UI for the deployed content:

1. Go to **Access** settings
2. Set visibility to the appropriate audience (e.g., specific groups or users)
3. If using SSO/LDAP/SAML, ensure the relevant groups are mapped

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `rsconnect: command not found` | `pip install rsconnect-python` |
| `403 Forbidden` during deploy | Check API key has publisher permissions |
| App deploys but shows blank page | Check Connect logs; likely a data file path issue |
| `FileNotFoundError` at runtime | Data/model files not in the bundle — use Option B |
| Plots don't render | Verify `plotly` is in `requirements.txt` (it is) |
| App is slow to start | Normal — it loads CSVs and pickle files at startup. First load takes ~5s. |
| `rsconnect deploy` hangs | Check network connectivity to the Connect server |

---

## Files Reference

| File | Purpose | Required for deploy? |
|------|---------|---------------------|
| `app/app.py` | Shiny app entry point | Yes |
| `app/requirements.txt` | Python dependencies | Yes |
| `app/modules/*.py` | Dashboard page modules | Yes |
| `app/utils/*.py` | Data loading and theming | Yes |
| `data/*.csv`, `data/*.json` | Simulated trial data | Yes |
| `models/*.pkl`, `models/*.json` | Trained ML models | Yes |
| `data/generate_trial_data.py` | Data generation script | No (development only) |
| `models/train_models.py` | Model training script | No (development only) |
| `quarto/*.qmd` | ETL report | No (separate deployment) |
| `DEPLOY.md` | Human deployment guide | No |
| `AI_AGENT_DEPLOY.md` | This file | No |
