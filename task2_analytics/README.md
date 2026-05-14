# Task 2 — Performance analytics & dashboarding

Interactive dashboard and written monitoring plan for Grammarly multi-campaign event data (`did_click_lp`, `did_install_grammarly`, `try_grammarly`).

## Deliverable overview

| Item | Location |
|------|----------|
| **Monitoring plan** (KPIs, rationale, panel mapping) | [`docs/monitoring_plan.md`](docs/monitoring_plan.md) |
| **Interactive dashboard** (4 panels) | Streamlit app [`app.py`](app.py) |
| **Dataset** (assignment extract) | [`data/grammarly_campaign_data.xlsx`](data/grammarly_campaign_data.xlsx) |
| **Transforms / definitions** | [`analytics_core.py`](analytics_core.py) |

## Run locally

```bash
cd task2_analytics
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

Opens a browser tab (default `http://localhost:8501`).

## What you’ll see

1. **Daily overview** — click & install time series, event-level daily CVR.  
2. **Campaign comparison** — user CVR by `lp_name` (first-touch attribution), volume bars, detail table.  
3. **Feature engagement** — `try_grammarly` mix by `product_feature`, funnel of unique users.  
4. **User funnel** — Sankey (click → install / drop; install → try / dormant), time-to-install distribution, retargeting list (click, no install) with CSV export.

Trademarks belong to their owners; this repo is a take-home exercise.
