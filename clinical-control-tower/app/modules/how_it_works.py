"""
How This Works Module
========================
Visual walkthrough of the full data science workflow powering the
Clinical Control Tower, highlighting how Posit's open-source and
professional products work together.
"""

from shiny import ui, render
from utils.theme import COLORS


def how_it_works_ui():
    return ui.nav_panel(
        "How This Works",
        ui.div(
            # Hero banner
            ui.HTML("""
            <div class="hero-banner">
                <h1>The Clinical Control Tower Architecture</h1>
                <p>A complete, production-grade data science workflow — from raw data ingestion
                to AI-powered insights — built entirely on the Posit ecosystem and open-source tools.</p>
                <div style="margin-top: 1.25rem; opacity: 0.8; font-size: 0.9rem;">
                    Governed &bull; Reproducible &bull; Scalable &bull; Auditable
                </div>
            </div>
            """),

            # ==========================================
            # WORKFLOW PIPELINE
            # ==========================================
            ui.HTML('<h3 style="color: var(--primary); font-weight: 700; margin-bottom: 1.5rem;">End-to-End Workflow Pipeline</h3>'),

            # Step 1: Data Ingestion
            ui.row(
                ui.column(12,
                    ui.HTML("""
                    <div class="workflow-step" style="border-left: 4px solid #2E86AB;">
                        <div style="display: flex; align-items: flex-start; gap: 1.5rem; text-align: left;">
                            <div style="min-width: 60px;">
                                <div class="step-icon">1</div>
                                <span class="step-tool">Quarto + Connect</span>
                            </div>
                            <div style="flex: 1;">
                                <div class="step-title" style="font-size: 1.15rem;">Data Ingestion & ETL Pipeline</div>
                                <div class="step-desc" style="margin-bottom: 1rem;">
                                    Raw data flows in from CTMS, EDC, IRT, central labs, and financial systems.
                                    A <strong>Quarto document</strong> orchestrates the entire ETL pipeline — extracting,
                                    validating, transforming, and loading data into the Control Tower's unified data layer.
                                </div>
                                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--secondary); margin-bottom: 0.4rem;">OPEN SOURCE</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>pandas</strong> for data manipulation &bull;
                                            <strong>SQLAlchemy</strong> for database connections &bull;
                                            <strong>Great Expectations</strong> for data validation
                                        </div>
                                    </div>
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: #1565C0; margin-bottom: 0.4rem;">POSIT VALUE-ADD</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Quarto on Connect</strong> runs on a schedule (daily/hourly) with
                                            email alerts on failure, execution history, and a complete audit trail.
                                            No Airflow, no cron, no DevOps — just deploy and schedule.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                class_="mb-2",
            ),
            ui.HTML('<div class="workflow-connector"><svg width="24" height="30" viewBox="0 0 24 30"><path d="M12 0 L12 24 M6 18 L12 24 L18 18" stroke="#2E86AB" stroke-width="2.5" fill="none"/></svg></div>'),

            # Step 2: Data Versioning
            ui.row(
                ui.column(12,
                    ui.HTML("""
                    <div class="workflow-step" style="border-left: 4px solid #A23B72;">
                        <div style="display: flex; align-items: flex-start; gap: 1.5rem; text-align: left;">
                            <div style="min-width: 60px;">
                                <div class="step-icon">2</div>
                                <span class="step-tool">Pins</span>
                            </div>
                            <div style="flex: 1;">
                                <div class="step-title" style="font-size: 1.15rem;">Versioned Data Artifacts</div>
                                <div class="step-desc" style="margin-bottom: 1rem;">
                                    Cleaned datasets are published as <strong>Pins</strong> — versioned, named data objects
                                    stored on Posit Connect. Every refresh creates a new version, enabling time-travel
                                    queries, reproducibility, and audit compliance.
                                </div>
                                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--secondary); margin-bottom: 0.4rem;">OPEN SOURCE</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>pins</strong> Python/R package for reading & writing versioned data artifacts.
                                            Works with local boards, S3, Azure, GCS, or Connect.
                                        </div>
                                    </div>
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: #1565C0; margin-bottom: 0.4rem;">POSIT VALUE-ADD</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Connect as a Pin Board</strong> provides governed, access-controlled storage.
                                            Data scientists pull the latest data with <code>board.pin_read("study-data")</code>.
                                            IT controls who can read/write. Full version history preserved.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                class_="mb-2",
            ),
            ui.HTML('<div class="workflow-connector"><svg width="24" height="30" viewBox="0 0 24 30"><path d="M12 0 L12 24 M6 18 L12 24 L18 18" stroke="#A23B72" stroke-width="2.5" fill="none"/></svg></div>'),

            # Step 3: Model Development
            ui.row(
                ui.column(12,
                    ui.HTML("""
                    <div class="workflow-step" style="border-left: 4px solid #F18F01;">
                        <div style="display: flex; align-items: flex-start; gap: 1.5rem; text-align: left;">
                            <div style="min-width: 60px;">
                                <div class="step-icon">3</div>
                                <span class="step-tool">Workbench + scikit-learn</span>
                            </div>
                            <div style="flex: 1;">
                                <div class="step-title" style="font-size: 1.15rem;">ML Model Development & Training</div>
                                <div class="step-desc" style="margin-bottom: 1rem;">
                                    Data scientists develop predictive models in <strong>Posit Workbench</strong> using
                                    their preferred IDE (VS Code, JupyterLab, or RStudio). Models include enrollment
                                    forecasting (gradient boosting), site risk classification (random forest), and
                                    composite site ranking algorithms.
                                </div>
                                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--secondary); margin-bottom: 0.4rem;">OPEN SOURCE</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>scikit-learn</strong> for ML models &bull;
                                            <strong>numpy/scipy</strong> for numerical computing &bull;
                                            <strong>pandas</strong> for feature engineering &bull;
                                            Python or R — your choice
                                        </div>
                                    </div>
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: #1565C0; margin-bottom: 0.4rem;">POSIT VALUE-ADD</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Posit Workbench</strong> provides governed, secure development environments.
                                            IT manages compute resources, controls data access via projects, and ensures
                                            reproducible environments. Session auditing tracks who accessed what data and when.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                class_="mb-2",
            ),
            ui.HTML('<div class="workflow-connector"><svg width="24" height="30" viewBox="0 0 24 30"><path d="M12 0 L12 24 M6 18 L12 24 L18 18" stroke="#F18F01" stroke-width="2.5" fill="none"/></svg></div>'),

            # Step 4: Model Management
            ui.row(
                ui.column(12,
                    ui.HTML("""
                    <div class="workflow-step" style="border-left: 4px solid #2E7D32;">
                        <div style="display: flex; align-items: flex-start; gap: 1.5rem; text-align: left;">
                            <div style="min-width: 60px;">
                                <div class="step-icon">4</div>
                                <span class="step-tool">Vetiver</span>
                            </div>
                            <div style="flex: 1;">
                                <div class="step-title" style="font-size: 1.15rem;">Model Versioning, Validation & APIs</div>
                                <div class="step-desc" style="margin-bottom: 1rem;">
                                    Trained models are wrapped in <strong>Vetiver</strong> for versioning, model cards,
                                    and deployment. Vetiver creates a complete record of model lineage — what data was
                                    used, what metrics were achieved, and who approved production deployment.
                                </div>
                                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--secondary); margin-bottom: 0.4rem;">OPEN SOURCE</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>vetiver</strong> for MLOps lifecycle management &bull;
                                            Model cards for documentation &bull;
                                            API generation with FastAPI &bull;
                                            Performance monitoring dashboards
                                        </div>
                                    </div>
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: #1565C0; margin-bottom: 0.4rem;">POSIT VALUE-ADD</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Vetiver on Connect</strong> deploys models as REST APIs with a single
                                            function call. Connect handles scaling, authentication, load balancing, and
                                            monitoring. No Docker, no Kubernetes, no MLflow server to maintain.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                class_="mb-2",
            ),
            ui.HTML('<div class="workflow-connector"><svg width="24" height="30" viewBox="0 0 24 30"><path d="M12 0 L12 24 M6 18 L12 24 L18 18" stroke="#2E7D32" stroke-width="2.5" fill="none"/></svg></div>'),

            # Step 5: Application Layer
            ui.row(
                ui.column(12,
                    ui.HTML("""
                    <div class="workflow-step" style="border-left: 4px solid #7B1FA2;">
                        <div style="display: flex; align-items: flex-start; gap: 1.5rem; text-align: left;">
                            <div style="min-width: 60px;">
                                <div class="step-icon">5</div>
                                <span class="step-tool">Shiny + Connect</span>
                            </div>
                            <div style="flex: 1;">
                                <div class="step-title" style="font-size: 1.15rem;">Interactive Application & Insight Delivery</div>
                                <div class="step-desc" style="margin-bottom: 1rem;">
                                    The Control Tower dashboard is built with <strong>Shiny for Python</strong> —
                                    providing real-time interactivity without JavaScript. Users explore enrollment
                                    forecasts, site rankings, and risk signals through an intuitive interface that
                                    calls model APIs and reads versioned data in real-time.
                                </div>
                                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--secondary); margin-bottom: 0.4rem;">OPEN SOURCE</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Shiny for Python</strong> for reactive dashboards &bull;
                                            <strong>Plotly</strong> for interactive charts &bull;
                                            <strong>pandas</strong> for data processing &bull;
                                            No JavaScript required
                                        </div>
                                    </div>
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: #1565C0; margin-bottom: 0.4rem;">POSIT VALUE-ADD</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Shiny on Connect</strong> scales to hundreds of concurrent users.
                                            Connect handles process management, authentication (SSO/LDAP/SAML),
                                            and usage analytics. Deploy with <code>rsconnect deploy shiny</code> — done.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                class_="mb-2",
            ),
            ui.HTML('<div class="workflow-connector"><svg width="24" height="30" viewBox="0 0 24 30"><path d="M12 0 L12 24 M6 18 L12 24 L18 18" stroke="#7B1FA2" stroke-width="2.5" fill="none"/></svg></div>'),

            # Step 6: Reporting & Compliance
            ui.row(
                ui.column(12,
                    ui.HTML("""
                    <div class="workflow-step" style="border-left: 4px solid #00838F;">
                        <div style="display: flex; align-items: flex-start; gap: 1.5rem; text-align: left;">
                            <div style="min-width: 60px;">
                                <div class="step-icon">6</div>
                                <span class="step-tool">Quarto + Email</span>
                            </div>
                            <div style="flex: 1;">
                                <div class="step-title" style="font-size: 1.15rem;">Automated Reporting & Compliance</div>
                                <div class="step-desc" style="margin-bottom: 1rem;">
                                    <strong>Quarto reports</strong> generate automated compliance documentation,
                                    audit trails, and executive summaries. Scheduled on Connect, they run
                                    alongside the ETL pipeline and deliver formatted reports via email
                                    to study teams, leadership, and regulatory stakeholders.
                                </div>
                                <div style="display: flex; gap: 1rem; flex-wrap: wrap;">
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: var(--secondary); margin-bottom: 0.4rem;">OPEN SOURCE</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Quarto</strong> for reproducible reporting in HTML, PDF, Word, PowerPoint &bull;
                                            Parameterized reports for per-study views &bull;
                                            Code + narrative in one document
                                        </div>
                                    </div>
                                    <div style="flex: 1; min-width: 200px;">
                                        <div style="font-weight: 600; font-size: 0.8rem; color: #1565C0; margin-bottom: 0.4rem;">POSIT VALUE-ADD</div>
                                        <div style="font-size: 0.85rem; color: var(--text-secondary);">
                                            <strong>Connect schedules & distributes reports</strong> automatically.
                                            Per-study variants render in parallel. Email delivery to stakeholder
                                            groups with access controls. Full execution history for 21 CFR Part 11
                                            compliance evidence.
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                class_="mb-4",
            ),

            # ==========================================
            # WHY POSIT CONNECT
            # ==========================================
            ui.HTML("""
            <div style="margin-top: 2rem;">
                <h3 style="color: var(--primary); font-weight: 700; margin-bottom: 1.5rem;">
                    Why Posit Connect is the Hub
                </h3>
                <p style="color: var(--text-secondary); font-size: 0.95rem; max-width: 800px; margin-bottom: 2rem;">
                    In the age of AI-powered data workflows, organizations need a platform that can deploy,
                    scale, and govern everything from ETL pipelines to ML APIs to interactive dashboards.
                    Posit Connect is that platform.
                </p>
            </div>
            """),

            # Pain points vs Connect solutions
            ui.row(
                ui.column(6,
                    ui.HTML("""
                    <div class="card" style="height: 100%;">
                        <div class="card-header" style="background: #FFF3E0 !important; color: #E65100;">
                            Without Posit Connect: The Typical Pain
                        </div>
                        <div class="card-body" style="padding: 1.25rem;">
                            <div style="font-size: 0.9rem; line-height: 1.8;">
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #E65100; font-weight: bold;">&#x2717;</span>
                                    <span><strong>Scheduling ETL?</strong> Set up Airflow/cron, manage a separate server, write DAGs, handle failures manually.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #E65100; font-weight: bold;">&#x2717;</span>
                                    <span><strong>Deploying ML APIs?</strong> Containerize with Docker, set up Kubernetes, configure load balancers, manage MLflow.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #E65100; font-weight: bold;">&#x2717;</span>
                                    <span><strong>Hosting dashboards?</strong> Provision servers, set up Nginx, configure SSL, manage scaling, build auth.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #E65100; font-weight: bold;">&#x2717;</span>
                                    <span><strong>Sharing data artifacts?</strong> Email CSVs, manage shared drives, lose version history, hope nothing breaks.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #E65100; font-weight: bold;">&#x2717;</span>
                                    <span><strong>Audit compliance?</strong> Manually track who ran what when, screenshot execution logs, pray during audits.</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #E65100; font-weight: bold;">&#x2717;</span>
                                    <span><strong>IT overhead?</strong> 5+ different platforms to secure, patch, monitor, and maintain. Months of setup time.</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                ui.column(6,
                    ui.HTML("""
                    <div class="card" style="height: 100%;">
                        <div class="card-header" style="background: #E8F5E9 !important; color: #2E7D32;">
                            With Posit Connect: One Platform
                        </div>
                        <div class="card-body" style="padding: 1.25rem;">
                            <div style="font-size: 0.9rem; line-height: 1.8;">
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #2E7D32; font-weight: bold;">&#x2713;</span>
                                    <span><strong>Scheduling ETL?</strong> Deploy Quarto doc, click "Schedule," set frequency. Email alerts on failure. Done.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #2E7D32; font-weight: bold;">&#x2713;</span>
                                    <span><strong>Deploying ML APIs?</strong> <code>vetiver.deploy_connect()</code>. Connect handles scaling, auth, versioning. One line.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #2E7D32; font-weight: bold;">&#x2713;</span>
                                    <span><strong>Hosting dashboards?</strong> <code>rsconnect deploy shiny</code>. SSO/LDAP/SAML built in. Auto-scaling included.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #2E7D32; font-weight: bold;">&#x2713;</span>
                                    <span><strong>Sharing data artifacts?</strong> Pins on Connect. Versioned, access-controlled, discoverable. One API call.</span>
                                </div>
                                <div style="margin-bottom: 0.75rem; display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #2E7D32; font-weight: bold;">&#x2713;</span>
                                    <span><strong>Audit compliance?</strong> Every deployment, execution, and access event is logged automatically. Always audit-ready.</span>
                                </div>
                                <div style="display: flex; align-items: flex-start; gap: 0.5rem;">
                                    <span style="color: #2E7D32; font-weight: bold;">&#x2713;</span>
                                    <span><strong>IT overhead?</strong> One platform to manage. Integrates with existing infrastructure. Days, not months.</span>
                                </div>
                            </div>
                        </div>
                    </div>
                    """),
                ),
                class_="mb-4 g-3",
            ),

            # ==========================================
            # TOOL ECOSYSTEM
            # ==========================================
            ui.HTML("""
            <div style="margin-top: 2rem;">
                <h3 style="color: var(--primary); font-weight: 700; margin-bottom: 0.5rem;">
                    The Posit Ecosystem in This Workflow
                </h3>
                <p style="color: var(--text-secondary); font-size: 0.9rem; margin-bottom: 1.5rem;">
                    Every tool in this Control Tower is either Posit-created open source or a widely-adopted
                    community package — deployed and governed through Posit's professional products.
                </p>
            </div>
            """),

            ui.row(
                # Commercial Products
                ui.column(4,
                    ui.HTML("""
                    <div class="tool-card">
                        <div class="tool-icon" style="background: #E3F2FD;">&#x1F310;</div>
                        <div class="tool-name">Posit Connect</div>
                        <span class="tool-type commercial">Professional</span>
                        <div class="tool-desc">
                            The deployment and scaling hub. Hosts Shiny apps, Quarto reports,
                            Vetiver APIs, Pins, and Jupyter notebooks. Handles auth, scheduling,
                            scaling, and audit logging. The single pane of glass for IT governance.
                        </div>
                    </div>
                    """),
                ),
                ui.column(4,
                    ui.HTML("""
                    <div class="tool-card">
                        <div class="tool-icon" style="background: #E3F2FD;">&#x1F4BB;</div>
                        <div class="tool-name">Posit Workbench</div>
                        <span class="tool-type commercial">Professional</span>
                        <div class="tool-desc">
                            The governed development environment. Data scientists use VS Code,
                            JupyterLab, or RStudio in managed sessions with controlled data access,
                            environment management, and session auditing.
                        </div>
                    </div>
                    """),
                ),
                ui.column(4,
                    ui.HTML("""
                    <div class="tool-card">
                        <div class="tool-icon" style="background: #E3F2FD;">&#x1F4E6;</div>
                        <div class="tool-name">Posit Package Manager</div>
                        <span class="tool-type commercial">Professional</span>
                        <div class="tool-desc">
                            Curated, validated package repositories for R and Python.
                            Ensures reproducible environments across development and production.
                            Validated packages for GxP compliance.
                        </div>
                    </div>
                    """),
                ),
                class_="mb-3 g-3",
            ),

            ui.row(
                # Open Source
                ui.column(3,
                    ui.HTML("""
                    <div class="tool-card">
                        <div class="tool-icon" style="background: #E8F5E9;">&#x2728;</div>
                        <div class="tool-name">Shiny for Python</div>
                        <span class="tool-type opensource">Open Source</span>
                        <div class="tool-desc">
                            Reactive web applications in pure Python. No JavaScript.
                            Powers this entire Control Tower dashboard.
                        </div>
                    </div>
                    """),
                ),
                ui.column(3,
                    ui.HTML("""
                    <div class="tool-card">
                        <div class="tool-icon" style="background: #E8F5E9;">&#x1F4D3;</div>
                        <div class="tool-name">Quarto</div>
                        <span class="tool-type opensource">Open Source</span>
                        <div class="tool-desc">
                            Scientific publishing system. Runs the ETL pipeline,
                            generates reports in HTML/PDF/Word, and creates documentation.
                        </div>
                    </div>
                    """),
                ),
                ui.column(3,
                    ui.HTML("""
                    <div class="tool-card">
                        <div class="tool-icon" style="background: #E8F5E9;">&#x1F4CC;</div>
                        <div class="tool-name">Pins</div>
                        <span class="tool-type opensource">Open Source</span>
                        <div class="tool-desc">
                            Versioned data artifacts. Publish and discover datasets,
                            models, and other objects with full version history.
                        </div>
                    </div>
                    """),
                ),
                ui.column(3,
                    ui.HTML("""
                    <div class="tool-card">
                        <div class="tool-icon" style="background: #E8F5E9;">&#x1F9EA;</div>
                        <div class="tool-name">Vetiver</div>
                        <span class="tool-type opensource">Open Source</span>
                        <div class="tool-desc">
                            MLOps lifecycle. Version models, create model cards,
                            deploy as APIs, and monitor performance over time.
                        </div>
                    </div>
                    """),
                ),
                class_="mb-4 g-3",
            ),

            # ==========================================
            # ARCHITECTURE DIAGRAM
            # ==========================================
            ui.HTML("""
            <div style="margin-top: 2rem;">
                <h3 style="color: var(--primary); font-weight: 700; margin-bottom: 1.5rem;">
                    Layered Architecture
                </h3>
            </div>
            """),

            ui.HTML("""
            <div style="max-width: 900px; margin: 0 auto 2rem auto;">
                <div class="arch-layer" style="border-color: #7B1FA2; background: linear-gradient(90deg, #F3E5F5 0%, white 30%);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="layer-name" style="color: #7B1FA2;">Presentation Layer</div>
                            <div class="layer-tools">Shiny for Python &bull; Plotly &bull; Quarto Reports</div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Interactive dashboards, alerts, reports</div>
                    </div>
                </div>
                <div style="text-align: center; color: #B0BEC5; font-size: 1.2rem; margin: 0.25rem 0;">&#x25BC;</div>
                <div class="arch-layer" style="border-color: #2E7D32; background: linear-gradient(90deg, #E8F5E9 0%, white 30%);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="layer-name" style="color: #2E7D32;">ML & Analytics Layer</div>
                            <div class="layer-tools">scikit-learn &bull; Vetiver &bull; Model APIs &bull; Signal Detection</div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Predictive models, risk algorithms, rankings</div>
                    </div>
                </div>
                <div style="text-align: center; color: #B0BEC5; font-size: 1.2rem; margin: 0.25rem 0;">&#x25BC;</div>
                <div class="arch-layer" style="border-color: #F18F01; background: linear-gradient(90deg, #FFF8E1 0%, white 30%);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="layer-name" style="color: #F18F01;">Data Management Layer</div>
                            <div class="layer-tools">Pins &bull; pandas &bull; Versioned Artifacts &bull; Feature Store</div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Governed, versioned data access</div>
                    </div>
                </div>
                <div style="text-align: center; color: #B0BEC5; font-size: 1.2rem; margin: 0.25rem 0;">&#x25BC;</div>
                <div class="arch-layer" style="border-color: #2E86AB; background: linear-gradient(90deg, #E3F2FD 0%, white 30%);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="layer-name" style="color: #2E86AB;">Ingestion & ETL Layer</div>
                            <div class="layer-tools">Quarto ETL &bull; SQLAlchemy &bull; API Connectors &bull; Validation</div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">Scheduled data pipelines</div>
                    </div>
                </div>
                <div style="text-align: center; color: #B0BEC5; font-size: 1.2rem; margin: 0.25rem 0;">&#x25BC;</div>
                <div class="arch-layer" style="border-color: #1B2A4A; background: linear-gradient(90deg, #E8EAF6 0%, white 30%);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div>
                            <div class="layer-name" style="color: #1B2A4A;">Source Systems</div>
                            <div class="layer-tools">CTMS &bull; EDC &bull; IRT/RTSM &bull; Central Labs &bull; Finance</div>
                        </div>
                        <div style="font-size: 0.8rem; color: var(--text-secondary);">External data sources</div>
                    </div>
                </div>
            </div>
            """),

            # ==========================================
            # DEPLOYMENT SECTION
            # ==========================================
            ui.HTML("""
            <div style="margin-top: 1rem;">
                <h3 style="color: var(--primary); font-weight: 700; margin-bottom: 1.5rem;">
                    Deploying This Control Tower
                </h3>
            </div>
            """),

            ui.HTML("""
            <div class="card" style="max-width: 900px; margin: 0 auto 2rem auto;">
                <div class="card-header">Deploy to Posit Connect in 3 Steps</div>
                <div class="card-body" style="padding: 1.5rem;">
                    <div style="font-family: 'SF Mono', 'Fira Code', monospace; font-size: 0.85rem;
                                background: #1B2A4A; color: #E8F4FD; border-radius: 8px; padding: 1.25rem;
                                line-height: 1.8; overflow-x: auto;">
                        <span style="color: #6B7280;"># Step 1: Install rsconnect-python</span><br>
                        <span style="color: #4FC3F7;">pip install</span> rsconnect-python<br><br>
                        <span style="color: #6B7280;"># Step 2: Configure your Connect server</span><br>
                        <span style="color: #4FC3F7;">rsconnect add</span> \\<br>
                        &nbsp;&nbsp;--server https://connect.example.com \\<br>
                        &nbsp;&nbsp;--name my-connect \\<br>
                        &nbsp;&nbsp;--api-key $CONNECT_API_KEY<br><br>
                        <span style="color: #6B7280;"># Step 3: Deploy the Control Tower</span><br>
                        <span style="color: #4FC3F7;">rsconnect deploy shiny</span> \\<br>
                        &nbsp;&nbsp;--server my-connect \\<br>
                        &nbsp;&nbsp;--title "Clinical Control Tower" \\<br>
                        &nbsp;&nbsp;./app/
                    </div>
                    <div style="margin-top: 1.25rem; font-size: 0.9rem; color: var(--text-secondary); line-height: 1.6;">
                        That's it. Connect handles SSL, authentication, process management, scaling,
                        and monitoring. No Docker files. No Kubernetes manifests. No CI/CD pipeline
                        to build. Just deploy and share the URL.
                    </div>
                </div>
            </div>
            """),

            # Future Vision callout
            ui.HTML("""
            <div class="posit-callout" style="max-width: 900px; margin: 0 auto 2rem auto;">
                <div class="callout-title">The AI-Powered Future</div>
                <div class="callout-body">
                    This Control Tower demonstrates the foundation. The next evolution includes:<br><br>
                    <strong>&#x2022; LLM-Powered Insights</strong> — Natural language queries against trial data
                    ("Why is Site 1042 underperforming?") powered by LLM APIs hosted on Connect.<br>
                    <strong>&#x2022; Agentic Workflows</strong> — AI agents that detect risks and automatically
                    draft mitigation plans for human review.<br>
                    <strong>&#x2022; Generative Reports</strong> — Quarto + LLMs generating narrative summaries
                    of weekly trial performance, tailored per stakeholder audience.<br><br>
                    All of this runs on the same Posit Connect platform — no new infrastructure required.
                </div>
            </div>
            """),

            class_="p-4",
        ),
        icon=ui.tags.i(class_="fa-solid fa-diagram-project"),
    )


def how_it_works_server(input, output, session):
    # This page is mostly static HTML content
    pass
