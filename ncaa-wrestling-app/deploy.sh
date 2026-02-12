#!/usr/bin/env bash
# =============================================================================
# NCAA Wrestling Tracker — Deployment Script for Posit Connect
# =============================================================================
#
# Deploys all 3 content items to Posit Connect:
#   1. Daily ETL (Quarto scheduled document)
#   2. Live Scores ETL (Quarto scheduled document)
#   3. Shiny App (interactive application)
#
# Prerequisites:
#   - rsconnect-python installed: pip install rsconnect-python
#   - Connect server configured: rsconnect add --name <name> --server <url> --api-key <key>
#
# Usage:
#   ./deploy.sh                    # Deploy all 3 items
#   ./deploy.sh --app-only         # Deploy just the Shiny app
#   ./deploy.sh --etl-only         # Deploy just the ETL jobs
#
# After deploying:
#   1. Set CONNECT_API_KEY in each content item's Environment settings
#   2. Set schedule for Daily ETL: daily at 6:00 AM ET
#   3. Set schedule for Live Scores ETL: every 1-5 minutes (or event days only)
#   4. Manually run Daily ETL once to seed initial data
# =============================================================================

set -euo pipefail

# --- Configuration ---
CONNECT_SERVER="${CONNECT_SERVER:?Set CONNECT_SERVER environment variable}"
CONNECT_API_KEY="${CONNECT_API_KEY:?Set CONNECT_API_KEY environment variable}"
PROJECT_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "============================================="
echo "NCAA Wrestling Tracker — Posit Connect Deploy"
echo "============================================="
echo "Server: ${CONNECT_SERVER}"
echo "Project: ${PROJECT_DIR}"
echo ""

deploy_etl() {
    echo "--- Deploying Daily ETL ---"
    rsconnect deploy quarto \
        --server "${CONNECT_SERVER}" \
        --api-key "${CONNECT_API_KEY}" \
        --entrypoint etl/notebooks/daily_etl.qmd \
        --title "NCAA Wrestling — Daily ETL" \
        "${PROJECT_DIR}"
    echo "  ✓ Daily ETL deployed"
    echo ""

    echo "--- Deploying Live Scores ETL ---"
    rsconnect deploy quarto \
        --server "${CONNECT_SERVER}" \
        --api-key "${CONNECT_API_KEY}" \
        --entrypoint etl/notebooks/live_scores_etl.qmd \
        --title "NCAA Wrestling — Live Scores" \
        "${PROJECT_DIR}"
    echo "  ✓ Live Scores ETL deployed"
    echo ""
}

deploy_app() {
    echo "--- Deploying Shiny App ---"
    rsconnect deploy shiny \
        --server "${CONNECT_SERVER}" \
        --api-key "${CONNECT_API_KEY}" \
        --entrypoint app/app.py \
        --title "NCAA Wrestling Tracker" \
        "${PROJECT_DIR}"
    echo "  ✓ Shiny App deployed"
    echo ""
}

# --- Parse arguments ---
case "${1:-all}" in
    --etl-only)
        deploy_etl
        ;;
    --app-only)
        deploy_app
        ;;
    all|*)
        deploy_etl
        deploy_app
        ;;
esac

echo "============================================="
echo "Deployment complete!"
echo ""
echo "NEXT STEPS:"
echo "  1. Open each content item on Connect"
echo "  2. Go to Settings → Environment and add:"
echo "       CONNECT_API_KEY = ${CONNECT_API_KEY}"
echo "  3. Set schedules:"
echo "       Daily ETL     → Schedule → Daily at 6:00 AM ET"
echo "       Live Scores   → Schedule → Every 5 minutes"
echo "  4. Manually run Daily ETL once to seed data"
echo "  5. Open the Shiny app — data should appear!"
echo "============================================="
