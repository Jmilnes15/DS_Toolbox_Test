"""How It Works page — architecture overview of the NCAA Wrestling Tracker."""

from shiny import module, ui


def _icon(emoji: str) -> ui.Tag:
    return ui.span(emoji, style="font-size:1.4rem; margin-right:0.4rem; vertical-align:middle;")


def _flow_arrow() -> ui.Tag:
    return ui.div(
        ui.div(class_="hiw-arrow-line"),
        ui.div(class_="hiw-arrow-head"),
        class_="hiw-flow-arrow",
    )


def _flow_arrow_label(label: str) -> ui.Tag:
    return ui.div(
        ui.div(class_="hiw-arrow-line"),
        ui.div(class_="hiw-arrow-head"),
        ui.div(label, class_="hiw-arrow-label"),
        class_="hiw-flow-arrow",
    )


def _tech_badge(text: str) -> ui.Tag:
    return ui.span(text, class_="hiw-tech-badge")


def _pin_chip(name: str) -> ui.Tag:
    return ui.span(name, class_="hiw-pin-chip")


def _section_header(number: str, title: str, subtitle: str) -> ui.Tag:
    return ui.div(
        ui.div(
            ui.span(number, class_="hiw-section-num"),
            ui.div(
                ui.span(title, class_="hiw-section-title"),
                ui.span(subtitle, class_="hiw-section-subtitle"),
            ),
            class_="hiw-section-header",
        ),
    )


def _detail_item(text: str, bold_prefix: str = "") -> ui.Tag:
    if bold_prefix:
        return ui.div(
            ui.span(bold_prefix, style="font-weight:600; color:#e0c45a;"),
            f" {text}",
            class_="hiw-detail-item",
        )
    return ui.div(text, class_="hiw-detail-item")


@module.ui
def how_it_works_ui():
    return ui.page_fluid(
        # ---- Hero Section ----
        ui.div(
            ui.h2(
                ui.span("How This App ", style="color:#fff;"),
                ui.span("Works", style="color:#c5a030;"),
                style="font-weight:800; margin:0;",
            ),
            ui.p(
                "A look under the hood at the data pipeline, architecture, and technology.",
                class_="hiw-hero-sub",
            ),
            ui.div(
                _tech_badge("Shiny for Python"),
                _tech_badge("Posit Connect"),
                _tech_badge("Posit Pins"),
                _tech_badge("Quarto"),
                _tech_badge("NCAA API"),
                _tech_badge("httpx"),
                _tech_badge("pandas"),
                class_="hiw-badge-row",
            ),
            class_="hiw-hero",
        ),

        # ==== SECTION 1: Data Sources ====
        _section_header("1", "External Data Sources",
                        "Public APIs serving live NCAA wrestling data"),
        ui.row(
            ui.column(
                6,
                ui.div(
                    ui.div(
                        _icon("\U0001F310"),
                        ui.span("NCAA API", style="font-weight:700; font-size:1rem;"),
                        style="margin-bottom:0.4rem;",
                    ),
                    ui.p(
                        "Community-maintained mirror of NCAA.com that returns clean JSON "
                        "instead of HTML. Covers all Division I sports.",
                        class_="hiw-card-desc",
                    ),
                    _detail_item("Live & final scores by date", "Scoreboard"),
                    _detail_item("NWCA Coaches Poll", "Rankings"),
                    _detail_item("Conference W/L by season", "Standings"),
                    _detail_item("Winning pct, falls, tech falls", "Team Stats"),
                    _detail_item("Wrestler wins and records", "Individual Stats"),
                    _detail_item("All NCAA school names and slugs", "Schools Index"),
                    _detail_item("Box scores and play-by-play", "Game Detail"),
                    ui.div(
                        _tech_badge("ncaa-api.henrygd.me"),
                        _tech_badge("Rate limit: 5 req/s"),
                        style="margin-top:0.6rem;",
                    ),
                    class_="hiw-card hiw-card-blue",
                ),
            ),
            ui.column(
                6,
                ui.div(
                    ui.div(
                        _icon("\U0001F3C6"),
                        ui.span("OpenTW API", style="font-weight:700; font-size:1rem;"),
                        style="margin-bottom:0.4rem;",
                    ),
                    ui.p(
                        "Middleware that parses TrackWrestling tournament pages into "
                        "structured JSON. Powers the bracket visualization.",
                        class_="hiw-card-desc",
                    ),
                    _detail_item("Event names, dates, metadata", "Tournament Details"),
                    _detail_item("Bout schedules and live status", "Match Assignments"),
                    _detail_item("Full bracket trees by weight class", "Bracket Data"),
                    ui.div(
                        _tech_badge("opentw-api.henrygd.me"),
                        _tech_badge("TrackWrestling Parser"),
                        style="margin-top:0.6rem;",
                    ),
                    class_="hiw-card hiw-card-blue",
                ),
            ),
            class_="hiw-row",
        ),

        _flow_arrow_label("JSON responses via httpx"),

        # ==== SECTION 2: ETL Pipeline ====
        _section_header("2", "ETL Pipeline",
                        "Python modules that fetch, transform, and load data"),
        ui.row(
            ui.column(
                6,
                ui.div(
                    ui.div(
                        _icon("\U0001F504"),
                        ui.span("API Client + Rate Limiter", style="font-weight:700;"),
                        style="margin-bottom:0.4rem;",
                    ),
                    ui.p(
                        "Handles all NCAA API calls with built-in rate limiting "
                        "(0.22s between requests), configurable timeout, and automatic "
                        "pagination for multi-page stat endpoints.",
                        class_="hiw-card-desc",
                    ),
                    _detail_item("13 endpoint methods covering every data type"),
                    _detail_item("get_scoreboard_range() iterates dates and merges games"),
                    _detail_item("get_all_team_stats() auto-paginates through all pages"),
                    ui.div(_tech_badge("etl/ncaa_api.py"), style="margin-top:0.6rem;"),
                    class_="hiw-card hiw-card-purple",
                ),
            ),
            ui.column(
                6,
                ui.div(
                    ui.div(
                        _icon("\U0001F9F9"),
                        ui.span("Data Transformers", style="font-weight:700;"),
                        style="margin-bottom:0.4rem;",
                    ),
                    ui.p(
                        "Four transformer modules clean raw API JSON into typed, "
                        "analysis-ready pandas DataFrames.",
                        class_="hiw-card-desc",
                    ),
                    _detail_item('Parses "School (votes)", computes rank movement', "rankings.py"),
                    _detail_item("Normalizes dynamic HTML table headers", "teams.py"),
                    _detail_item("Flattens nested game objects, classifies state", "scores.py"),
                    _detail_item("Builds unified schedule from scoreboard range", "schedules.py"),
                    ui.div(_tech_badge("etl/transformers/"), style="margin-top:0.6rem;"),
                    class_="hiw-card hiw-card-purple",
                ),
            ),
            class_="hiw-row",
        ),
        ui.row(
            ui.column(
                6,
                ui.div(
                    ui.div(
                        _icon("\U0001F4C5"),
                        ui.span("Daily ETL Orchestrator", style="font-weight:700;"),
                        style="margin-bottom:0.4rem;",
                    ),
                    ui.p(
                        "Runs the full pipeline in sequence \u2014 fetches 6 datasets from "
                        "the NCAA API, transforms each one, and writes 6 pins.",
                        class_="hiw-card-desc",
                    ),
                    _detail_item("Rankings (current NWCA poll)"),
                    _detail_item("Team Stats (all pages, stat_id=170)"),
                    _detail_item("Individual Stats (all pages, stat_id=171)"),
                    _detail_item("Standings (current season)"),
                    _detail_item("Schools Index (full NCAA directory)"),
                    _detail_item("Schedule (past 7 days + next 30 days)"),
                    ui.div(
                        _tech_badge("run_daily.py"),
                        _tech_badge("Scheduled: 6 AM ET"),
                        style="margin-top:0.6rem;",
                    ),
                    class_="hiw-card hiw-card-amber",
                ),
            ),
            ui.column(
                6,
                ui.div(
                    ui.div(
                        _icon("\u26A1"),
                        ui.span("Live Scores Fetcher", style="font-weight:700;"),
                        style="margin-bottom:0.4rem;",
                    ),
                    ui.p(
                        "Lightweight single-endpoint job \u2014 fetches today's scoreboard "
                        "and overwrites the live_scores pin. Built for high-frequency execution.",
                        class_="hiw-card-desc",
                    ),
                    _detail_item("Fetches scoreboard for today's date"),
                    _detail_item("Transforms to 24-column DataFrame"),
                    _detail_item("Writes ncaa_wrestling/live_scores pin"),
                    _detail_item("Logs live vs. final vs. upcoming counts"),
                    ui.div(
                        _tech_badge("run_live.py"),
                        _tech_badge("Scheduled: every 1\u20135 min"),
                        style="margin-top:0.6rem;",
                    ),
                    class_="hiw-card hiw-card-amber",
                ),
            ),
            class_="hiw-row",
        ),

        _flow_arrow_label('pins.board.pin_write(df, type="parquet")'),

        # ==== SECTION 3: Connect Pins Board ====
        _section_header("3", "Posit Connect Pins Board",
                        "Shared data layer \u2014 the glue between ETL and the app"),
        ui.div(
            ui.div(
                ui.h4(
                    "pins.board_connect()",
                    style="font-weight:700; color:#fff; text-align:center; margin-bottom:0.25rem;",
                ),
                ui.p(
                    "Versioned, managed data objects on Posit Connect. ETL jobs write "
                    "DataFrames here as Parquet files; the Shiny app reads them. "
                    "No shared filesystem, no database, no custom API needed.",
                    style="text-align:center; margin-bottom:1rem;",
                    class_="hiw-card-desc",
                ),
                ui.div(
                    _pin_chip("ncaa_wrestling/rankings"),
                    _pin_chip("ncaa_wrestling/team_stats"),
                    _pin_chip("ncaa_wrestling/individual_stats"),
                    _pin_chip("ncaa_wrestling/standings"),
                    _pin_chip("ncaa_wrestling/schools"),
                    _pin_chip("ncaa_wrestling/schedule"),
                    _pin_chip("ncaa_wrestling/live_scores"),
                    class_="hiw-pin-row",
                ),
                class_="hiw-pins-board",
            ),
        ),
        # Horizontal flow
        ui.div(
            ui.div(
                ui.div("ETL Writes", class_="hiw-hflow-title"),
                ui.div("Quarto jobs push DataFrames as Parquet", class_="hiw-hflow-desc"),
                class_="hiw-hflow-item",
            ),
            ui.span("\u2192", class_="hiw-hflow-arrow"),
            ui.div(
                ui.div("Connect Board", class_="hiw-hflow-title"),
                ui.div("Versioned storage with metadata", class_="hiw-hflow-desc"),
                class_="hiw-hflow-item hiw-hflow-item-accent",
            ),
            ui.span("\u2192", class_="hiw-hflow-arrow"),
            ui.div(
                ui.div("App Reads", class_="hiw-hflow-title"),
                ui.div("Shiny loads fresh data on each request", class_="hiw-hflow-desc"),
                class_="hiw-hflow-item",
            ),
            class_="hiw-hflow",
        ),

        _flow_arrow_label("pins.board.pin_read() \u2192 pandas DataFrame"),

        # ==== SECTION 4: Shiny App ====
        _section_header("4", "Shiny for Python Application",
                        "6-page interactive web app with modular architecture"),
        ui.row(
            ui.column(4, ui.div(
                ui.div(_icon("\U0001F4CA"), ui.span("Dashboard", style="font-weight:700;"),
                       style="margin-bottom:0.3rem;"),
                _detail_item("4 value boxes: #1 team, ranked count, live now, upcoming"),
                _detail_item("Top 10 rankings with rank badges & trend arrows"),
                _detail_item("Recent results table with scores"),
                _detail_item("Conference standings preview"),
                ui.div(_tech_badge("Reads: 4 pins"), style="margin-top:0.5rem;"),
                class_="hiw-card hiw-card-green",
            )),
            ui.column(4, ui.div(
                ui.div(_icon("\U0001F3C5"), ui.span("Rankings", style="font-weight:700;"),
                       style="margin-bottom:0.3rem;"),
                _detail_item("Top-N slider (5\u2013100)"),
                _detail_item("Team search filter"),
                _detail_item("Gold/blue rank badges (top 5, 10, 25)"),
                _detail_item("Movement trend indicators"),
                ui.div(_tech_badge("Reads: rankings"), style="margin-top:0.5rem;"),
                class_="hiw-card hiw-card-green",
            )),
            ui.column(4, ui.div(
                ui.div(_icon("\U0001F4C6"), ui.span("Schedule", style="font-weight:700;"),
                       style="margin-bottom:0.3rem;"),
                _detail_item("View modes: All / Upcoming / Results"),
                _detail_item("Team search across home & away"),
                _detail_item("Network filter (ESPN, BTN, Flo)"),
                _detail_item("Formatted matchups with ranks & scores"),
                ui.div(_tech_badge("Reads: schedule"), style="margin-top:0.5rem;"),
                class_="hiw-card hiw-card-green",
            )),
            class_="hiw-row",
        ),
        ui.row(
            ui.column(4, ui.div(
                ui.div(_icon("\U0001F3EB"), ui.span("Teams", style="font-weight:700;"),
                       style="margin-bottom:0.3rem;"),
                _detail_item("Toggle: Standings vs. Stats view"),
                _detail_item("Dynamic conference dropdown"),
                _detail_item("Team search filter"),
                _detail_item("Conf W/L, Overall W/L, Streak"),
                ui.div(_tech_badge("Reads: standings, team_stats"), style="margin-top:0.5rem;"),
                class_="hiw-card hiw-card-green",
            )),
            ui.column(4, ui.div(
                ui.div(_icon("\U0001F534"), ui.span("Live Scores", style="font-weight:700;"),
                       style="margin-bottom:0.3rem;"),
                _detail_item("Score cards with live pulse animation"),
                _detail_item("Status filter: Live / Final / Upcoming"),
                _detail_item("3 count boxes with totals"),
                _detail_item("Manual refresh re-reads pin"),
                ui.div(_tech_badge("Reads: live_scores"), style="margin-top:0.5rem;"),
                class_="hiw-card hiw-card-green",
            )),
            ui.column(4, ui.div(
                ui.div(_icon("\U0001F3AF"), ui.span("Brackets", style="font-weight:700;"),
                       style="margin-bottom:0.3rem;"),
                _detail_item("Weight class selector (125\u2013285 lbs)"),
                _detail_item("Round filter (R32 \u2192 Finals)"),
                _detail_item("Bracket match components with seeds"),
                _detail_item("Placeholder during off-season"),
                ui.div(_tech_badge("Reads: brackets"), style="margin-top:0.5rem;"),
                class_="hiw-card hiw-card-green",
            )),
            class_="hiw-row",
        ),

        _flow_arrow(),

        # ==== SECTION 5: Connect Platform ====
        _section_header("5", "Posit Connect \u2014 The Platform Layer",
                        "Hosts, schedules, and connects all the pieces"),
        ui.div(
            ui.p(
                "Three independently deployed content items that communicate through "
                "a shared pins board \u2014 no glue code, no cron jobs on a VM, "
                "no S3 buckets to manage.",
                class_="hiw-card-desc",
                style="text-align:center; margin-bottom:1.25rem;",
            ),
            class_="hiw-connect-intro",
        ),
        ui.row(
            ui.column(4, ui.div(
                ui.div("1", class_="hiw-deploy-num"),
                ui.div("Daily ETL", style="font-weight:700; font-size:0.95rem; margin-bottom:0.2rem;"),
                ui.p("Quarto document rendered on schedule. Connect runs it, captures "
                     "the output as an HTML report, and logs success/failure.",
                     class_="hiw-card-desc"),
                ui.div("rsconnect deploy quarto", class_="hiw-cmd"),
                ui.div("--entrypoint etl/notebooks/daily_etl.qmd", class_="hiw-cmd"),
                ui.p(
                    ui.span("Schedule: ", style="color:#c5a030; font-weight:600;"),
                    "Daily at 6:00 AM ET",
                    style="margin-top:0.5rem; font-size:0.82rem;",
                ),
                class_="hiw-card hiw-card-deploy",
            )),
            ui.column(4, ui.div(
                ui.div("2", class_="hiw-deploy-num"),
                ui.div("Live Scores ETL", style="font-weight:700; font-size:0.95rem; margin-bottom:0.2rem;"),
                ui.p("Lightweight Quarto doc for high-frequency refresh. "
                     "Same deploy pattern, different schedule.",
                     class_="hiw-card-desc"),
                ui.div("rsconnect deploy quarto", class_="hiw-cmd"),
                ui.div("--entrypoint etl/notebooks/live_scores_etl.qmd", class_="hiw-cmd"),
                ui.p(
                    ui.span("Schedule: ", style="color:#c5a030; font-weight:600;"),
                    "Every 1\u20135 min on event days",
                    style="margin-top:0.5rem; font-size:0.82rem;",
                ),
                class_="hiw-card hiw-card-deploy",
            )),
            ui.column(4, ui.div(
                ui.div("3", class_="hiw-deploy-num"),
                ui.div("Shiny App", style="font-weight:700; font-size:0.95rem; margin-bottom:0.2rem;"),
                ui.p("Always-on interactive application. Connect handles scaling, "
                     "auth, load balancing, and TLS.",
                     class_="hiw-card-desc"),
                ui.div("rsconnect deploy shiny", class_="hiw-cmd"),
                ui.div("--entrypoint app/app.py", class_="hiw-cmd"),
                ui.p(
                    ui.span("Mode: ", style="color:#c5a030; font-weight:600;"),
                    "Always-on application",
                    style="margin-top:0.5rem; font-size:0.82rem;",
                ),
                class_="hiw-card hiw-card-deploy",
            )),
            class_="hiw-row",
        ),

        # ==== Connect Value Props ====
        ui.div(
            ui.h4("Where Posit Connect Adds Value",
                   style="text-align:center; font-weight:700; color:#1a2744; margin-bottom:1rem;"),
            class_="hiw-vp-header",
        ),
        ui.row(
            ui.column(4, ui.div(
                ui.div("\U0001F4C5", class_="hiw-vp-icon"),
                ui.div("Managed Scheduling", class_="hiw-vp-title"),
                ui.p("No cron, no Airflow, no Lambda. Connect's built-in scheduler "
                     "runs Quarto ETL jobs on whatever cadence you set \u2014 daily, "
                     "hourly, or every minute.", class_="hiw-vp-desc"),
                class_="hiw-vp-card",
            )),
            ui.column(4, ui.div(
                ui.div("\U0001F517", class_="hiw-vp-icon"),
                ui.div("Pins as Data Contracts", class_="hiw-vp-title"),
                ui.p("The pins board is a versioned, shared namespace. ETL writes "
                     "DataFrames, the app reads them. Producers and consumers are "
                     "completely decoupled.", class_="hiw-vp-desc"),
                class_="hiw-vp-card",
            )),
            ui.column(4, ui.div(
                ui.div("\U0001F512", class_="hiw-vp-icon"),
                ui.div("Zero-Config Auth", class_="hiw-vp-title"),
                ui.p("CONNECT_SERVER is auto-injected at runtime. Pins auth is handled "
                     "by Connect's internal token exchange \u2014 no secrets in code, "
                     "no .env files on servers.", class_="hiw-vp-desc"),
                class_="hiw-vp-card",
            )),
            class_="hiw-row",
        ),
        ui.row(
            ui.column(4, ui.div(
                ui.div("\U0001F680", class_="hiw-vp-icon"),
                ui.div("One-Command Deploys", class_="hiw-vp-title"),
                ui.p("Each content item deploys with a single rsconnect CLI command. "
                     "Connect builds the Python environment from requirements.txt "
                     "automatically.", class_="hiw-vp-desc"),
                class_="hiw-vp-card",
            )),
            ui.column(4, ui.div(
                ui.div("\U0001F4C8", class_="hiw-vp-icon"),
                ui.div("ETL Observability", class_="hiw-vp-title"),
                ui.p("Every Quarto render produces an HTML report saved on Connect. "
                     "If the daily ETL fails, you see exactly which step broke \u2014 "
                     "it's a rendered notebook, not a log file.", class_="hiw-vp-desc"),
                class_="hiw-vp-card",
            )),
            ui.column(4, ui.div(
                ui.div("\U0001F310", class_="hiw-vp-icon"),
                ui.div("Environment Parity", class_="hiw-vp-title"),
                ui.p("Local dev uses pins.board_folder() with the same read/write API. "
                     "Flip to board_connect() with one env var. No code changes "
                     "between laptop and production.", class_="hiw-vp-desc"),
                class_="hiw-vp-card",
            )),
            class_="hiw-row",
        ),

        # ==== Section 6: Environment Detection ====
        _section_header("6", "Environment Detection",
                        "How the code knows where it's running"),
        ui.div(
            ui.div(
                ui.h4("Dual-Mode Board Selection",
                       style="font-weight:700; text-align:center; margin-bottom:0.5rem;"),
                ui.p(
                    "Both the ETL writer and the app reader check for the ",
                    ui.code("CONNECT_SERVER"),
                    " environment variable. If present (auto-injected by Posit Connect), "
                    "they use ",
                    ui.code("pins.board_connect()"),
                    ". If absent (local laptop), they use ",
                    ui.code('pins.board_folder("pin_cache/")'),
                    ". Same code, same API, zero conditional logic in the business layer.",
                    style="text-align:center; max-width:720px; margin:0 auto;",
                    class_="hiw-card-desc",
                ),
                ui.div(
                    ui.div(
                        ui.div("On Connect", class_="hiw-env-label"),
                        _pin_chip("CONNECT_SERVER=https://connect.example.com"),
                        class_="hiw-env-block",
                    ),
                    ui.div(
                        ui.div("Locally", class_="hiw-env-label"),
                        ui.span("(not set) \u2192 pin_cache/", class_="hiw-pin-chip",
                                style="opacity:0.6;"),
                        class_="hiw-env-block",
                    ),
                    class_="hiw-env-row",
                ),
                class_="hiw-card hiw-card-env",
            ),
        ),
    )


@module.server
def how_it_works_server(input, output, session):
    pass
