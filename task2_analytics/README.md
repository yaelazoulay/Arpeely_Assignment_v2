# Task 2 — Performance analytics & dashboarding

What the brief asks for | Where it is
---|---
**Functional visualization report (live)** | **https://arpeelyassignmentv2-r5sbba7txppecvjrmxdcgt.streamlit.app/** (Streamlit Community Cloud) — or run [`app.py`](app.py) locally.  
**Brief summary (1–2 paragraphs)** | Expand *Summary* in the Streamlit app, or [`docs/metrics-rationale-summary.md`](docs/metrics-rationale-summary.md).  
**Deeper monitoring plan** | [`docs/monitoring_plan.md`](docs/monitoring_plan.md)

---

Interactive dashboard and written monitoring plan for Grammarly multi-campaign event data (`did_click_lp`, `did_install_grammarly`, `try_grammarly`).

## Deploy / share Streamlit yourself

1. Push this repo to GitHub.  
2. Sign in at [streamlit.io/cloud](https://streamlit.io/cloud), **New app** → pick the repo, **Main file path:** `task2_analytics/app.py` (or set the app root to `task2_analytics` if the UI offers it).  
3. Set app visibility to **Public** so reviewers can open it without logging in.  
4. Use the `*.streamlit.app` URL in your application email or README.

## Deliverable overview

| Item | Location |
|------|----------|
| **Summary (1–2 paragraphs)** | [`docs/metrics-rationale-summary.md`](docs/metrics-rationale-summary.md) + in-app expander |
| **Monitoring plan** (extended) | [`docs/monitoring_plan.md`](docs/monitoring_plan.md) |
| **Interactive dashboard** | [`app.py`](app.py) |
| **Dataset** | [`data/grammarly_campaign_data.xlsx`](data/grammarly_campaign_data.xlsx) |
| **Transforms** | [`analytics_core.py`](analytics_core.py) |

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
