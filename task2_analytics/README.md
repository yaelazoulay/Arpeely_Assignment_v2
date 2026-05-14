# Task 2 — Performance analytics & dashboarding

What the brief asks for | Where it is
---|---
**Functional visualization report** | Interactive **Streamlit** dashboard: [`app.py`](app.py). **Public link:** deploy once (see below) and paste your URL next to “Live app” in your email or PR. **Local:** `streamlit run app.py` → `http://localhost:8501`.
**Brief summary (1–2 paragraphs): why these metrics & how they measure success** | [`docs/reviewer_summary.md`](docs/reviewer_summary.md) — *same text is inside the dashboard* (expandable section at the top: *Summary — why these metrics…*).
**Deeper monitoring plan** (optional detail) | [`docs/monitoring_plan.md`](docs/monitoring_plan.md)

---

Interactive dashboard and written monitoring plan for Grammarly multi-campaign event data (`did_click_lp`, `did_install_grammarly`, `try_grammarly`).

## Get a shareable link (Streamlit Community Cloud)

1. Push this repo (or a fork) to GitHub.  
2. Sign in at [streamlit.io/cloud](https://streamlit.io/cloud), **New app** → pick the repo, **main file path:** `task2_analytics/app.py` (or set app root to `task2_analytics` per Cloud UI).  
3. Copy the `*.streamlit.app` URL — that is your **link to the functional visualization report**.

If you do not deploy, reviewers can still run locally (section below).

## Deliverable overview

| Item | Location |
|------|----------|
| **Summary (1–2 paragraphs)** | [`docs/reviewer_summary.md`](docs/reviewer_summary.md) + in-app expander |
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
