# NCAA Wrestling Tracker — Comprehensive App Plan

## 1. Vision & Overview

An interactive web application deployed on **Posit Connect** that serves as the definitive dashboard for NCAA Division I wrestling. The primary user is a wrestling enthusiast who wants a single place to track rankings, schedules, live scores, team stats, and tournament brackets across the entire NCAA season (November–March).

### Core User Stories

| # | As a user, I want to... | Priority |
|---|-------------------------|----------|
| 1 | See current top-ranked wrestlers at each of the 10 weight classes | Must-have |
| 2 | View team rankings and interesting team-level stats | Must-have |
| 3 | Browse all upcoming duals and tournaments with date, time, channel, and location | Must-have |
| 4 | View bracket information for tournaments | Must-have |
| 5 | See real-time (or near-real-time) scores during live matches and tournaments | Must-have |
| 6 | Search for a specific wrestler or team and see their full profile | Should-have |
| 7 | Filter schedules by conference, team, or weight class | Should-have |
| 8 | See head-to-head comparison tools for wrestlers | Nice-to-have |
| 9 | Get notified when my favorite team/wrestler is competing | Nice-to-have |

---

## 2. Architecture Overview

The system follows a **three-layer architecture** optimized for Posit Connect:

```
┌─────────────────────────────────────────────────────────┐
│                    POSIT CONNECT                        │
│                                                         │
│  ┌──────────────┐   ┌──────────────┐   ┌─────────────┐ │
│  │  Scheduled    │   │  Posit Pins  │   │  Shiny App  │ │
│  │  ETL Jobs     │──▶│  (Data Store)│◀──│  (Frontend) │ │
│  │  (Python)     │   │              │   │  (Python)   │ │
│  └──────┬───────┘   └──────────────┘   └──────┬──────┘ │
│         │                                      │        │
│         ▼                                      ▼        │
│  ┌──────────────┐                    ┌──────────────┐   │
│  │ External APIs │                    │   Users /    │   │
│  │ & Scrapers    │                    │   Browsers   │   │
│  └──────────────┘                    └──────────────┘   │
└─────────────────────────────────────────────────────────┘
```

### Layer 1 — Data Ingestion (ETL Pipeline)

Scheduled Python scripts that run on Posit Connect as background jobs to fetch, clean, and store data.

### Layer 2 — Data Storage (Posit Pins)

Versioned, cached datasets stored via the `pins` library. The Shiny app reads from pins rather than hitting APIs directly, ensuring fast load times and resilience against API outages.

### Layer 3 — Interactive Frontend (Shiny for Python)

A polished Shiny for Python application with multiple tabs/pages for each major feature area.

---

## 3. Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **App Framework** | Shiny for Python | Native Posit Connect support, reactive/real-time UI, rich interactivity, Python ecosystem access |
| **UI Layer** | `shiny` + `shinywidgets` + custom CSS/HTML | Polished, modern look with custom theming |
| **Data Processing** | `pandas`, `polars` | Fast tabular data manipulation |
| **Data Storage** | `pins` (Python) | Native Posit Connect integration, versioned datasets, caching |
| **Data Ingestion** | `httpx` / `requests`, `beautifulsoup4`, `lxml` | API calls + HTML scraping for sources without APIs |
| **Visualizations** | `plotly`, `great_tables` | Interactive charts and publication-quality tables |
| **Scheduling** | Posit Connect Scheduled Reports (Quarto) | Trigger ETL pipelines on cron schedules |
| **Deployment** | Posit Connect | Company instance, `rsconnect-python` CLI for publishing |
| **Version Control** | Git | This repository |
| **Environment** | `requirements.txt` + Python venv | Reproducible dependencies |

---

## 4. Data Sources & Ingestion Strategy

### 4.1 Primary Data Source: NCAA API (henrygd/ncaa-api)

The best free, structured data source. This open-source project mirrors NCAA.com URL paths and returns JSON. It can be self-hosted via Docker for reliability, or hit the public instance at `https://ncaa-api.henrygd.me`.

**Available endpoints for wrestling:**

| Data | Endpoint Pattern | Refresh Rate |
|------|-----------------|-------------|
| Live Scoreboard | `/scoreboard/wrestling/d1/{year}/{month}/{day}/all-conf` | Every 60 seconds during live events |
| Rankings (Coaches Poll) | `/rankings/wrestling/d1/current` | Weekly |
| Team Stats | `/stats/wrestling/d1/current/team/{stat-id}` | Daily |
| Individual Stats | `/stats/wrestling/d1/current/individual/{stat-id}` | Daily |
| Standings | `/standings/wrestling/d1` | Daily |
| Game Box Score | `/game/{game-id}/boxscore` | Post-match |
| Play-by-Play | `/game/{game-id}/play-by-play` | Live/post-match |
| School Directory | `/schools-index` | Seasonal |

### 4.2 Secondary Source: OpenTW API (TrackWrestling)

Structured tournament/bracket data parsed from TrackWrestling.

| Data | Endpoint Pattern | Refresh Rate |
|------|-----------------|-------------|
| Tournament Details | `/tournaments/{type}/{id}` | Per-tournament |
| Match Assignments | `/tournaments/{type}/{id}/matches` | Live during events |
| Bracket Data | `/tournaments/{type}/{id}/brackets` | Live during events |

### 4.3 Tertiary Sources (Web Scraping)

For data not available via API, targeted scraping of select pages:

| Source | Data | Method |
|--------|------|--------|
| WrestleStat.com | Wrestler rankings per weight class, dual projections | `beautifulsoup4` scraping |
| InterMat | Tournament Power Index (TPI) rankings | `beautifulsoup4` scraping |
| ESPN.com | TV schedule, broadcast info for wrestling events | `beautifulsoup4` scraping |
| NCAA.com (direct) | Championship bracket PDFs, schedule pages | `beautifulsoup4` / PDF parsing |

### 4.4 Static/Reference Data

Maintained as version-controlled CSV/JSON files in the repo:

- Weight classes (125, 133, 141, 149, 157, 165, 174, 184, 197, 285)
- Conference membership lists
- School metadata (name, mascot, logo URL, conference, location)
- TV channel lookup table (ESPN, ESPN2, ESPNU, ESPN+, BTN, B1G+, FloWrestling, etc.)

### 4.5 Data Refresh Schedule

| Dataset | Refresh Frequency | Trigger |
|---------|-------------------|---------|
| Rankings | Once daily (6 AM ET) | Posit Connect scheduled job |
| Team/Individual Stats | Once daily (6 AM ET) | Posit Connect scheduled job |
| Standings | Once daily (6 AM ET) | Posit Connect scheduled job |
| Schedule/Upcoming Events | Twice daily (6 AM, 6 PM ET) | Posit Connect scheduled job |
| Live Scores | Every 60 seconds | In-app reactive polling (during events) |
| Bracket Data | Every 2 minutes during active tournaments | In-app reactive polling |
| School/Reference Data | Seasonally (manual update) | Git commit |

---

## 5. Data Models

### 5.1 Core Entities

```
┌─────────────┐     ┌─────────────────┐     ┌──────────────┐
│   School     │     │    Wrestler      │     │  WeightClass │
│─────────────│     │─────────────────│     │──────────────│
│ school_id    │◀───│ school_id (FK)   │     │ weight       │
│ name         │     │ wrestler_id      │────▶│ (125...285)  │
│ mascot       │     │ name             │     └──────────────┘
│ conference   │     │ weight_class     │
│ logo_url     │     │ year             │     ┌──────────────┐
│ location     │     │ record (W-L)     │     │   Ranking    │
│ primary_color│     │ ranking          │     │──────────────│
│ division     │     │ seed             │     │ wrestler_id  │
└──────┬──────┘     └────────┬────────┘     │ poll_source  │
       │                     │               │ rank         │
       │                     │               │ weight_class │
       ▼                     ▼               │ as_of_date   │
┌─────────────┐     ┌─────────────────┐     └──────────────┘
│  TeamStats   │     │     Match        │
│─────────────│     │─────────────────│
│ school_id    │     │ match_id         │
│ wins         │     │ event_id (FK)    │
│ losses       │     │ wrestler1_id     │
│ conf_wins    │     │ wrestler2_id     │
│ conf_losses  │     │ weight_class     │
│ team_rank    │     │ result           │
│ dual_rank    │     │ score            │
│ pin_count    │     │ win_type         │
│ bonus_rate   │     │ period           │
│ maj_dec_pct  │     │ duration         │
└─────────────┘     │ status (live/    │
                    │   final/upcoming)│
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
                    │     Event        │
                    │─────────────────│
                    │ event_id         │
                    │ name             │
                    │ type (dual/      │
                    │   tournament)    │
                    │ date             │
                    │ time             │
                    │ location         │
                    │ venue            │
                    │ broadcast_channel│
                    │ stream_url       │
                    │ bracket_url      │
                    │ status           │
                    └─────────────────┘
```

---

## 6. App Layout & UX Design

### 6.1 Navigation Structure

The app uses a top-level tabbed navigation with the following pages:

```
┌──────────────────────────────────────────────────────────────┐
│  🤼 NCAA Wrestling Tracker         [Search] [Refresh] [⚙]  │
├──────────────────────────────────────────────────────────────┤
│  Dashboard │ Rankings │ Schedule │ Live │ Teams │ Brackets   │
├──────────────────────────────────────────────────────────────┤
│                                                              │
│                    (Page Content Area)                        │
│                                                              │
└──────────────────────────────────────────────────────────────┘
```

### 6.2 Page Descriptions

#### Page 1: Dashboard (Home)

The landing page — an at-a-glance overview of what matters right now.

**Layout:**
```
┌─────────────────────────────────────────────────────┐
│  SEASON BANNER: "2025-26 NCAA Division I Wrestling" │
├─────────────────────┬───────────────────────────────┤
│                     │                               │
│  TODAY'S ACTION     │   RANKINGS SNAPSHOT           │
│  ┌───────────────┐  │   Weight: [125 ▼]             │
│  │ Live Now (2)  │  │   ┌───┬──────────┬──────────┐ │
│  │ Iowa vs PSU   │  │   │ 1 │ Spencer  │ Iowa     │ │
│  │  Score: 12-9  │  │   │ 2 │ Glory    │ PSU      │ │
│  │               │  │   │ 3 │ ...      │ ...      │ │
│  │ Upcoming (5)  │  │   └───┴──────────┴──────────┘ │
│  │ 7:00 PM ...   │  │                               │
│  └───────────────┘  │   TOP 25 TEAMS                │
│                     │   ┌───┬──────────┬────┐       │
│  RECENT RESULTS     │   │ 1 │ Penn St  │32-0│       │
│  ┌───────────────┐  │   │ 2 │ Iowa     │28-2│       │
│  │ Iowa 24       │  │   │ 3 │ ...      │    │       │
│  │ Minnesota 12  │  │   └───┴──────────┴────┘       │
│  └───────────────┘  │                               │
│                     │   NEWS TICKER / NOTABLE        │
│                     │   "Upset alert: #15 beats #2"  │
├─────────────────────┴───────────────────────────────┤
│  UPCOMING THIS WEEK (scrollable event cards)        │
│  [Card] [Card] [Card] [Card] →                      │
└─────────────────────────────────────────────────────┘
```

**Key Components:**
- Live event indicator with auto-refreshing scores
- Quick-glance rankings widget with weight class selector
- Top 25 team rankings table
- Upcoming events carousel
- Recent results feed

#### Page 2: Rankings

Deep dive into wrestler and team rankings.

**Features:**
- Weight class selector (tabs or dropdown for all 10 classes)
- Sortable, searchable table per weight class showing: Rank, Wrestler, School, Record, Conference, Movement (up/down arrows)
- Team rankings table with: Rank, School, Dual Record, Conference Record, Bonus Rate, Pin Count
- Source toggle: NWCA Coaches Poll vs. other available rankings
- Sparkline trend charts showing ranking movement over the season
- Click any wrestler row to expand and see recent match history

#### Page 3: Schedule & Events

Comprehensive calendar of all NCAA wrestling events.

**Features:**
- Calendar view (month) and list view toggle
- Filter by: Conference, Team, Event Type (Dual, Tournament, Championship), Broadcast Channel
- Each event card shows:
  - Date & Time (with timezone)
  - Teams/Participants
  - Location & Venue
  - Broadcast channel with logo (ESPN, BTN, FloWrestling, etc.)
  - Link to stream (if available)
  - "Add to Calendar" export (`.ics`)
- Countdown timer for the NCAA Championships
- Conference championship schedule section

#### Page 4: Live Scores

Real-time scoreboard for active matches and tournaments.

**Features:**
- Auto-refreshing every 60 seconds (configurable)
- "Live Now" section at top with active dual meets and tournament sessions
- Match-by-match scoring within a dual:
  ```
  IOWA vs PENN STATE — Live
  ─────────────────────────────────────
  125 lb  │ Spencer Lee (IOWA)  maj.dec  John Doe (PSU)     │ 12-4  ✓
  133 lb  │ Real Wrestler (IOWA) vs Another (PSU)           │ LIVE  3-2 P2
  141 lb  │ TBD vs TBD                                       │ Upcoming
  ...
  ─────────────────────────────────────
  Team Score: Iowa 10 — Penn State 3
  ```
- Tournament scoring view with bracket progress
- Visual "mat assignment" view during tournaments (which mat, what time)
- Push-style notification banners for upsets or pins

#### Page 5: Teams

Team profiles and comparison tools.

**Features:**
- Searchable team directory (all D1 wrestling programs)
- Team profile page showing:
  - School logo, name, conference, coach
  - Season record (overall and conference)
  - Full roster by weight class with individual records
  - Schedule (past results + upcoming)
  - Team stats: wins, losses, pins, tech falls, major decisions, bonus rate
- Team comparison tool: side-by-side stats for two teams
- Conference standings view
- Sortable team statistics leaderboards

#### Page 6: Brackets & Tournaments

Tournament bracket visualization and tracking.

**Features:**
- Interactive bracket viewer for active and completed tournaments
- NCAA Championship bracket (when available)
- Conference championship brackets
- Click any wrestler in a bracket to see their path
- Bracket projection/simulation tool (stretch goal)
- PDF bracket download

### 6.3 UI/UX Design Principles

1. **Dark/Light Mode**: Support both themes (dark mode preferred for sports apps)
2. **Responsive**: Works on desktop and tablet (primary targets)
3. **Color System**: Use school colors contextually; neutral palette for chrome
4. **Typography**: Clean, sans-serif fonts. Large, scannable numbers for scores and rankings
5. **Loading States**: Skeleton loaders for data-heavy sections, never blank screens
6. **Accessibility**: WCAG 2.1 AA compliance — proper contrast ratios, alt text, keyboard navigation
7. **Performance**: Sub-3-second initial load via pins caching; reactive polling only on active pages

---

## 7. Project Structure

```
ncaa-wrestling-app/
├── PLAN.md                          # This document
├── requirements.txt                 # Python dependencies
├── manifest.json                    # Posit Connect deployment manifest
│
├── app/                             # Shiny for Python application
│   ├── app.py                       # Main Shiny app entry point
│   ├── modules/                     # Shiny modules (one per page)
│   │   ├── __init__.py
│   │   ├── dashboard.py             # Dashboard/home page module
│   │   ├── rankings.py              # Rankings page module
│   │   ├── schedule.py              # Schedule/events page module
│   │   ├── live_scores.py           # Live scores page module
│   │   ├── teams.py                 # Teams page module
│   │   └── brackets.py             # Brackets page module
│   ├── components/                  # Reusable UI components
│   │   ├── __init__.py
│   │   ├── event_card.py            # Event card component
│   │   ├── ranking_table.py         # Ranking table component
│   │   ├── score_ticker.py          # Live score ticker component
│   │   ├── bracket_viewer.py        # Bracket visualization component
│   │   └── team_card.py             # Team profile card component
│   ├── utils/                       # Shared utilities
│   │   ├── __init__.py
│   │   ├── data_loader.py           # Pin reading utilities
│   │   ├── formatters.py            # Score/record formatting helpers
│   │   └── constants.py             # Weight classes, conferences, etc.
│   └── www/                         # Static assets
│       ├── css/
│       │   └── styles.css           # Custom app styles
│       ├── img/                     # Logos, icons
│       └── js/
│           └── custom.js            # Custom JavaScript (if needed)
│
├── etl/                             # Data ingestion pipeline
│   ├── __init__.py
│   ├── config.py                    # API URLs, scraping targets, schedule config
│   ├── ncaa_api.py                  # NCAA API client
│   ├── opentw_api.py                # OpenTW/TrackWrestling API client
│   ├── scrapers/                    # Web scrapers
│   │   ├── __init__.py
│   │   ├── wrestlestat.py           # WrestleStat scraper
│   │   ├── intermat.py              # InterMat TPI scraper
│   │   └── espn_schedule.py         # ESPN broadcast schedule scraper
│   ├── transformers/                # Data cleaning & transformation
│   │   ├── __init__.py
│   │   ├── rankings.py              # Rankings data transformation
│   │   ├── schedules.py             # Schedule data transformation
│   │   ├── scores.py                # Scores data transformation
│   │   └── teams.py                 # Team data transformation
│   ├── pin_writer.py                # Write processed data to Posit Pins
│   ├── run_daily.py                 # Daily ETL orchestrator
│   └── run_live.py                  # Live score fetching (called by app)
│
├── data/                            # Static reference data
│   ├── weight_classes.json          # Weight class definitions
│   ├── conferences.json             # Conference membership
│   ├── schools.json                 # School metadata
│   └── broadcast_channels.json      # TV/streaming channel info
│
├── notebooks/                       # Exploration & development notebooks
│   ├── 01_api_exploration.qmd       # Explore NCAA API responses
│   ├── 02_data_modeling.qmd         # Prototype data transformations
│   └── 03_ui_prototyping.qmd        # UI component prototyping
│
├── scheduled/                       # Posit Connect scheduled documents
│   ├── daily_etl.qmd                # Quarto doc scheduled to run daily ETL
│   └── live_score_check.qmd         # Quarto doc for periodic live checks
│
└── tests/                           # Unit & integration tests
    ├── __init__.py
    ├── test_ncaa_api.py
    ├── test_transformers.py
    └── test_data_loader.py
```

---

## 8. Implementation Phases

### Phase 1: Foundation & Data Pipeline (Weeks 1-2)

**Goal:** Establish project structure, connect to data sources, and build the ETL pipeline.

**Tasks:**
- [ ] Set up Python project with `requirements.txt` and virtual environment
- [ ] Create reference data files (schools, conferences, weight classes, channels)
- [ ] Build NCAA API client (`etl/ncaa_api.py`) with error handling and rate limiting
- [ ] Build data transformers for rankings, standings, stats, and schedules
- [ ] Set up Posit Pins board and implement `pin_writer.py`
- [ ] Build and test `run_daily.py` ETL orchestrator
- [ ] Deploy daily ETL as a scheduled Quarto doc on Posit Connect
- [ ] Validate data quality with exploration notebooks

**Deliverable:** Working data pipeline that populates pins with rankings, standings, stats, and schedule data on a daily schedule.

### Phase 2: Core App — Rankings, Schedule, Teams (Weeks 3-4)

**Goal:** Build the Shiny app skeleton and the three core pages.

**Tasks:**
- [ ] Set up Shiny for Python app scaffold (`app.py`, module structure)
- [ ] Implement `data_loader.py` to read from pins
- [ ] Build Rankings page with weight class tabs, sortable tables, trend indicators
- [ ] Build Schedule page with calendar/list views, filters, event cards
- [ ] Build Teams page with team directory, profiles, roster views
- [ ] Implement custom CSS theme (dark/light mode support)
- [ ] Deploy initial app to Posit Connect
- [ ] Add search functionality across wrestlers and teams

**Deliverable:** Deployed Shiny app on Posit Connect with Rankings, Schedule, and Teams pages fully functional.

### Phase 3: Live Scores & Dashboard (Weeks 5-6)

**Goal:** Add real-time capabilities and the dashboard landing page.

**Tasks:**
- [ ] Build live score fetching module (`etl/run_live.py`)
- [ ] Implement Live Scores page with auto-refreshing reactive polling
- [ ] Build dual meet scoreboard component (match-by-match view)
- [ ] Build Dashboard page assembling widgets from other pages
- [ ] Add "Live Now" indicator and event status detection
- [ ] Implement recent results feed on dashboard
- [ ] Performance optimization — ensure reactive polling doesn't degrade UX
- [ ] Test live score flow during actual wrestling events

**Deliverable:** Full dashboard with live scoring capabilities during active events.

### Phase 4: Brackets & Polish (Weeks 7-8)

**Goal:** Add bracket visualization, polish UI, and harden for production use.

**Tasks:**
- [ ] Integrate OpenTW API for tournament bracket data
- [ ] Build interactive bracket viewer component
- [ ] Implement bracket page with tournament selection
- [ ] Add bracket progression tracking (click a wrestler → see their path)
- [ ] UI polish pass: loading states, error handling, empty states, transitions
- [ ] Cross-browser and responsiveness testing
- [ ] Performance audit and optimization
- [ ] Write user documentation / help tooltips
- [ ] Final Posit Connect deployment configuration (access controls, scaling)

**Deliverable:** Production-ready app with full bracket support and polished UX.

### Phase 5: Stretch Goals (Ongoing)

- [ ] Head-to-head wrestler comparison tool
- [ ] Bracket prediction/simulation engine
- [ ] Push notifications for favorite teams/wrestlers
- [ ] Historical season data and year-over-year comparison
- [ ] Mobile-optimized layout
- [ ] "What to watch tonight" recommendation widget
- [ ] Integration with FloWrestling subscription for enriched data
- [ ] Community features (picks, predictions)

---

## 9. Key Dependencies & Requirements

### Python Packages

```
# Core App
shiny>=1.0.0
shinywidgets>=0.3.0
htmltools>=0.5.0

# Data Processing
pandas>=2.0.0
polars>=0.20.0

# Data Storage
pins>=0.8.0

# Visualization
plotly>=5.18.0
great-tables>=0.2.0

# Data Ingestion
httpx>=0.27.0
beautifulsoup4>=4.12.0
lxml>=5.0.0

# Deployment
rsconnect-python>=1.22.0

# Utilities
python-dateutil>=2.8.0
pytz>=2024.1
pydantic>=2.0.0

# Testing
pytest>=8.0.0
pytest-asyncio>=0.23.0
```

### External Services

| Service | Purpose | Cost | Required? |
|---------|---------|------|-----------|
| NCAA API (henrygd) | Primary data source (rankings, scores, stats) | Free (public) or self-host via Docker | Yes |
| OpenTW API | Tournament brackets and match data | Free (self-host) | Yes |
| Posit Connect | App hosting, scheduled jobs, pins storage | Company instance (already available) | Yes |
| WrestleStat.com | Supplemental rankings | Free (scraping) | Optional |
| InterMat | TPI rankings | Free (scraping) | Optional |
| ESPN.com | Broadcast schedule data | Free (scraping) | Optional |

### Infrastructure Requirements

| Requirement | Details |
|-------------|---------|
| Posit Connect instance | Company-provided, with permissions to deploy Shiny apps and schedule Quarto docs |
| Python 3.11+ | On the Posit Connect server |
| Outbound internet access | From Posit Connect to NCAA API and scraping targets |
| Pin board | Posit Connect pins board (auto-provisioned) |
| Git access | For CI/CD from this repository to Posit Connect |

---

## 10. Risks & Mitigations

| Risk | Impact | Likelihood | Mitigation |
|------|--------|------------|------------|
| NCAA API goes offline or changes | Loss of primary data source | Medium | Self-host the NCAA API via Docker; cache data aggressively in pins; implement fallback scraping |
| Web scraping targets change HTML structure | Broken scrapers | High (over time) | Isolate scrapers into individual modules; add monitoring/alerting; use CSS selectors resilient to minor changes |
| Rate limiting on public NCAA API (5 req/sec) | Throttled data fetching | Low | Self-host the API; implement request queuing and backoff |
| Real-time scores latency | Scores lag behind actual events | Medium | Document that "real-time" means ~60-second delay; explore WebSocket alternatives if available |
| Posit Connect resource limits | App crashes under load or scheduled jobs fail | Low | Profile memory/CPU usage; optimize pin sizes; use efficient data formats (parquet) |
| FloWrestling/TrackWrestling blocks scraping | Loss of bracket/tournament data | Medium | Rely on OpenTW API (community-maintained); cache historical data; provide manual data entry fallback |
| Season-dependent content | App feels empty during off-season | Certain | Show historical data, preseason rankings, and countdown to next season during off-season |

---

## 11. Success Metrics

| Metric | Target |
|--------|--------|
| Data freshness — rankings | Updated within 24 hours of new poll release |
| Data freshness — live scores | Within 60 seconds of actual score change |
| App load time | < 3 seconds to interactive |
| Coverage — weight classes | All 10 weight classes with complete top-33 rankings |
| Coverage — schedule | All D1 duals and major tournaments listed |
| Coverage — broadcast info | Channel/stream info for all televised events |
| User satisfaction | Enthusiast can answer "What's happening in NCAA wrestling right now?" in < 10 seconds |

---

## 12. Deployment Strategy

### Initial Deployment

1. Publish the Shiny app to Posit Connect using `rsconnect-python`
2. Deploy the daily ETL Quarto document as a scheduled report
3. Configure pin board permissions
4. Set access controls (who can view the app)

### CI/CD Pipeline (Recommended)

```
Git Push → Posit Connect Git-backed Deployment
   └── Automatic re-deploy on push to main branch
```

Alternatively, use `rsconnect deploy shiny` from a CI pipeline (GitHub Actions or similar).

### Monitoring

- Posit Connect built-in job monitoring for scheduled ETL
- Application logs via Posit Connect dashboard
- Data freshness checks (last-updated timestamps displayed in app footer)

---

## 13. What You Need to Get Started

To turn this plan into reality, you will need:

1. **Access & Permissions**
   - Posit Connect admin or publisher access on your company instance
   - Ability to deploy Shiny for Python apps
   - Ability to schedule Quarto documents
   - Outbound internet access from the Connect server

2. **Development Environment**
   - Python 3.11+
   - An IDE (VS Code, RStudio, or similar)
   - Git

3. **Data Source Validation**
   - Test the NCAA API endpoints to confirm wrestling data availability for the current season
   - Verify the OpenTW API can access relevant tournament data
   - Identify the specific stat IDs and poll names for wrestling on NCAA.com

4. **Design Assets**
   - School logos (available via NCAA API `/schools-index`)
   - Channel logos (ESPN, BTN, FloWrestling — source from their press kits)
   - App logo/branding

5. **Time & Effort**
   - A development team or individual with Python and Shiny experience
   - Phases 1-4 represent the core build
   - Phase 5 contains enhancements that can be added iteratively

---

## Summary

This plan delivers a **Shiny for Python** application deployed on **Posit Connect** that gives wrestling fans a comprehensive, interactive dashboard for the NCAA D1 wrestling season. It uses the free **henrygd/ncaa-api** as its primary data source, supplemented by the **OpenTW API** for bracket data and targeted web scraping for broadcast schedules and supplemental rankings.

The architecture separates data ingestion (scheduled ETL → Pins) from the interactive frontend, ensuring fast load times and resilience. The app covers six core areas: Dashboard, Rankings, Schedule, Live Scores, Teams, and Brackets — each designed to answer the wrestling fan's key questions at a glance.
