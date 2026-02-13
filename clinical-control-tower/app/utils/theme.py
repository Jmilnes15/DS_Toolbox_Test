"""
Theme and styling constants for the Clinical Control Tower.
"""

# Color palette - clinical/pharma inspired
COLORS = {
    "primary": "#1B2A4A",       # Deep navy
    "secondary": "#2E86AB",     # Clinical blue
    "accent": "#A23B72",        # Magenta accent
    "success": "#2E7D32",       # Green
    "warning": "#F57F17",       # Amber
    "danger": "#C62828",        # Red
    "info": "#0277BD",          # Info blue
    "light_bg": "#F5F7FA",      # Light background
    "card_bg": "#FFFFFF",       # Card background
    "text_primary": "#1A1A2E",  # Primary text
    "text_secondary": "#6B7280",# Secondary text
    "border": "#E5E7EB",        # Border color

    # Chart colors
    "chart_1": "#2E86AB",
    "chart_2": "#A23B72",
    "chart_3": "#F18F01",
    "chart_4": "#2E7D32",
    "chart_5": "#7B1FA2",
    "chart_6": "#00838F",

    # Risk colors
    "risk_low": "#4CAF50",
    "risk_medium": "#FF9800",
    "risk_high": "#F44336",
    "risk_critical": "#B71C1C",

    # Tier colors
    "tier_top": "#1B5E20",
    "tier_good": "#4CAF50",
    "tier_below": "#FF9800",
    "tier_under": "#F44336",
}

PLOTLY_TEMPLATE = {
    "layout": {
        "paper_bgcolor": "rgba(0,0,0,0)",
        "plot_bgcolor": "rgba(0,0,0,0)",
        "font": {"family": "Inter, system-ui, sans-serif", "color": COLORS["text_primary"]},
        "title": {"font": {"size": 16, "color": COLORS["primary"]}},
        "xaxis": {"gridcolor": "#E5E7EB", "linecolor": "#E5E7EB"},
        "yaxis": {"gridcolor": "#E5E7EB", "linecolor": "#E5E7EB"},
        "colorway": [
            COLORS["chart_1"], COLORS["chart_2"], COLORS["chart_3"],
            COLORS["chart_4"], COLORS["chart_5"], COLORS["chart_6"],
        ],
        "margin": {"t": 50, "b": 40, "l": 50, "r": 20},
    }
}


def risk_color(level):
    """Return color for a risk level."""
    return {
        "Low": COLORS["risk_low"],
        "Medium": COLORS["risk_medium"],
        "High": COLORS["risk_high"],
        "Critical": COLORS["risk_critical"],
    }.get(level, COLORS["text_secondary"])


def tier_color(tier):
    """Return color for a performance tier."""
    return {
        "Top Performer": COLORS["tier_top"],
        "Good": COLORS["tier_good"],
        "Below Average": COLORS["tier_below"],
        "Underperforming": COLORS["tier_under"],
    }.get(tier, COLORS["text_secondary"])


# Global CSS for the application
APP_CSS = """
:root {
    --primary: #1B2A4A;
    --secondary: #2E86AB;
    --accent: #A23B72;
    --success: #2E7D32;
    --warning: #F57F17;
    --danger: #C62828;
    --light-bg: #F5F7FA;
    --card-bg: #FFFFFF;
    --text-primary: #1A1A2E;
    --text-secondary: #6B7280;
    --border: #E5E7EB;
}

body {
    font-family: 'Inter', system-ui, -apple-system, sans-serif;
    background-color: var(--light-bg);
    color: var(--text-primary);
}

.navbar {
    background-color: var(--primary) !important;
    box-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.navbar .nav-link {
    color: rgba(255,255,255,0.85) !important;
    font-weight: 500;
    padding: 0.5rem 1rem !important;
    border-radius: 6px;
    transition: all 0.2s;
}

.navbar .nav-link:hover,
.navbar .nav-link.active {
    color: #ffffff !important;
    background-color: rgba(255,255,255,0.15);
}

.bslib-value-box {
    border: none !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.08), 0 1px 2px rgba(0,0,0,0.06) !important;
    transition: transform 0.2s, box-shadow 0.2s;
}

.bslib-value-box:hover {
    transform: translateY(-2px);
    box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
}

.card {
    border: 1px solid var(--border) !important;
    border-radius: 12px !important;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06) !important;
    overflow: hidden;
}

.card-header {
    background-color: var(--card-bg) !important;
    border-bottom: 1px solid var(--border) !important;
    font-weight: 600;
    color: var(--primary);
    padding: 1rem 1.25rem !important;
}

.kpi-metric {
    text-align: center;
    padding: 1.25rem;
}

.kpi-metric .value {
    font-size: 2rem;
    font-weight: 700;
    color: var(--primary);
    line-height: 1.2;
}

.kpi-metric .label {
    font-size: 0.8rem;
    color: var(--text-secondary);
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-top: 0.25rem;
}

.kpi-metric .trend {
    font-size: 0.85rem;
    margin-top: 0.25rem;
}

.kpi-metric .trend.up { color: var(--success); }
.kpi-metric .trend.down { color: var(--danger); }

.signal-badge {
    display: inline-block;
    padding: 0.2em 0.65em;
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 0.03em;
}

.signal-critical { background: #FFEBEE; color: #B71C1C; }
.signal-high { background: #FFF3E0; color: #E65100; }
.signal-medium { background: #FFF8E1; color: #F57F17; }
.signal-low { background: #E8F5E9; color: #2E7D32; }

.status-badge {
    display: inline-block;
    padding: 0.25em 0.75em;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 500;
}

.status-enrolling { background: #E3F2FD; color: #1565C0; }
.status-active { background: #E8F5E9; color: #2E7D32; }
.status-completed { background: #F3E5F5; color: #7B1FA2; }
.status-startup { background: #FFF8E1; color: #F57F17; }

.workflow-step {
    background: white;
    border: 2px solid var(--border);
    border-radius: 16px;
    padding: 1.5rem;
    text-align: center;
    transition: all 0.3s;
    position: relative;
}

.workflow-step:hover {
    border-color: var(--secondary);
    box-shadow: 0 4px 16px rgba(46, 134, 171, 0.15);
    transform: translateY(-3px);
}

.workflow-step .step-icon {
    font-size: 2.5rem;
    margin-bottom: 0.75rem;
}

.workflow-step .step-title {
    font-weight: 700;
    color: var(--primary);
    font-size: 1rem;
    margin-bottom: 0.5rem;
}

.workflow-step .step-desc {
    font-size: 0.85rem;
    color: var(--text-secondary);
    line-height: 1.4;
}

.workflow-step .step-tool {
    display: inline-block;
    margin-top: 0.75rem;
    padding: 0.25em 0.75em;
    background: var(--light-bg);
    border-radius: 20px;
    font-size: 0.75rem;
    font-weight: 600;
    color: var(--secondary);
}

.workflow-connector {
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    color: var(--secondary);
    padding: 0.5rem 0;
}

.posit-callout {
    background: linear-gradient(135deg, #EBF5FB 0%, #F0E6F6 100%);
    border-left: 4px solid var(--secondary);
    border-radius: 0 12px 12px 0;
    padding: 1.25rem 1.5rem;
    margin: 1rem 0;
}

.posit-callout .callout-title {
    font-weight: 700;
    color: var(--primary);
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.posit-callout .callout-body {
    font-size: 0.9rem;
    color: var(--text-primary);
    line-height: 1.5;
}

.table-container {
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid var(--border);
}

.table thead th {
    background-color: var(--primary) !important;
    color: white !important;
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    padding: 0.75rem 1rem;
    border: none !important;
}

.table tbody td {
    padding: 0.65rem 1rem;
    font-size: 0.875rem;
    vertical-align: middle;
    border-color: var(--border);
}

.table tbody tr:hover {
    background-color: #F8FAFC;
}

.section-header {
    color: var(--primary);
    font-weight: 700;
    font-size: 1.15rem;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid var(--secondary);
    display: inline-block;
}

.filter-panel {
    background: white;
    border-radius: 12px;
    border: 1px solid var(--border);
    padding: 1rem 1.25rem;
    margin-bottom: 1.25rem;
}

.filter-panel label {
    font-weight: 600;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    color: var(--text-secondary);
}

/* How it works page */
.hero-banner {
    background: linear-gradient(135deg, var(--primary) 0%, #2E86AB 100%);
    color: white;
    padding: 2.5rem 2rem;
    border-radius: 16px;
    margin-bottom: 2rem;
    text-align: center;
}

.hero-banner h1 {
    font-size: 2rem;
    font-weight: 800;
    margin-bottom: 0.75rem;
}

.hero-banner p {
    font-size: 1.1rem;
    opacity: 0.9;
    max-width: 700px;
    margin: 0 auto;
}

.tool-card {
    background: white;
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.5rem;
    height: 100%;
    transition: all 0.3s;
}

.tool-card:hover {
    border-color: var(--secondary);
    box-shadow: 0 4px 16px rgba(0,0,0,0.08);
}

.tool-card .tool-icon {
    width: 48px;
    height: 48px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.5rem;
    margin-bottom: 1rem;
}

.tool-card .tool-name {
    font-weight: 700;
    font-size: 1.05rem;
    color: var(--primary);
    margin-bottom: 0.5rem;
}

.tool-card .tool-type {
    display: inline-block;
    padding: 0.15em 0.5em;
    border-radius: 4px;
    font-size: 0.7rem;
    font-weight: 600;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.tool-card .tool-type.commercial { background: #E3F2FD; color: #1565C0; }
.tool-card .tool-type.opensource { background: #E8F5E9; color: #2E7D32; }

.tool-card .tool-desc {
    font-size: 0.875rem;
    color: var(--text-secondary);
    line-height: 1.5;
}

.arch-layer {
    background: white;
    border: 2px solid var(--border);
    border-radius: 12px;
    padding: 1.25rem;
    margin-bottom: 0.75rem;
    transition: all 0.3s;
}

.arch-layer:hover {
    border-color: var(--secondary);
}

.arch-layer .layer-name {
    font-weight: 700;
    color: var(--primary);
    font-size: 0.95rem;
}

.arch-layer .layer-tools {
    font-size: 0.85rem;
    color: var(--text-secondary);
}
"""
