# Campaign monitoring plan — Grammarly growth

This note defines **what we monitor daily**, **how we compute it** from the event extract, and **how each dashboard panel answers a growth question**. It pairs with the Streamlit prototype in the same folder.

---

## 1. Context

Grammarly runs parallel feature-led campaigns (e.g. academic writing, business email). Events tie **media → LP → install → in-product trial**. The dashboard goal is **same-day visibility** on volume, conversion quality, and post-install behavior so the team can react within 24 hours (creative fatigue, tracking drops, LP regressions).

---

## 2. Data we have

| Field | Use |
|-------|-----|
| `session_id` | Session grain (not primary for funnel KPIs here) |
| `user_id` | Funnel, cohorts, retargeting lists |
| `action` | `did_click_lp`, `did_install_grammarly`, `try_grammarly` |
| `extra` | JSON: `lp_name` on LP clicks; `product_feature` on trials |
| `timestamp` | Daily trends, time-to-install |

**Limits (called out in-product):**

- **Impressions** are not in the file, so **LP CTR** (clicks ÷ impressions) cannot be computed here; we anchor on **click volume** and **install CVR** instead.
- **Install** rows carry empty `extra`; we **attribute installs to LP with first-touch** — the `lp_name` on the user’s **earliest** `did_click_lp`. This matches a common growth convention and unlocks campaign-level install CVR.

---

## 3. KPIs & business questions

| KPI | Definition (this dataset) | Question it answers |
|-----|----------------------------|---------------------|
| **Click volume** | Count of `did_click_lp` (daily / total) | Are we filling the top of the funnel? |
| **Install volume** | Count of `did_install_grammarly` (daily) | Are installs keeping pace with clicks? |
| **User CVR** | Unique users with install ÷ unique users with LP click | Are we converting intent, not just counting raw events? |
| **Event CVR (daily)** | Installs ÷ clicks **on the same calendar day** | Fast diagnostic for daily pacing (not a substitute for user CVR). |
| **LP install CVR** | Installs (first-touch attrib.) ÷ unique clickers per `lp_name` | Which LP is winning on quality? |
| **Feature adoption** | Unique users with `try_grammarly` ÷ installers | Do installers actually engage with the product? |
| **Top features tried** | Count of `try_grammarly` by `product_feature` | What use cases resonate after install? |
| **Time to install** | `min(timestamp_install) − min(timestamp_click)` per user | Proxy for intent; fast converters often merit separate messaging or bids. |
| **Retargeting pool** | Users with `did_click_lp` and **no** `did_install_grammarly` | Who should see install-focused follow-up? |

---

## 4. Dashboard panels (mapping)

| Panel | Charts / artifacts | Decision use |
|-------|-------------------|--------------|
| **1 · Daily overview** | Line: daily clicks & installs; bar: event CVR by day; headline KPIs | Catch **anomalies** (volume cliff, CVR swing vs prior day). |
| **2 · Campaign comparison** | Bar: user CVR by `lp_name`; grouped bars: click events vs attributed install users; table | Rank **LPs**; align budget and creative tests. |
| **3 · Feature engagement** | Horizontal bar: trials by `product_feature`; funnel of unique users (click → install → try) | Link acquisition to **product discovery**; spot onboarding gaps when CVR is fine but adoption is weak. |
| **4 · User funnel** | Sankey: click → install / no install; install → try / dormant; histogram: time-to-install; table + CSV: no-install clickers | **Diagnose drop-offs**; export audiences for retargeting. |

---

## 5. Why this set hangs together

Together these metrics cover **awareness proxy** (clicks), **conversion** (install CVR by user and by LP), and **early retention signal** (trials per installer). Segmenting by `lp_name` and `product_feature` keeps the view actionable without external warehouses for v1.

Daily **install CVR** and **daily active installs** are the fastest tripwires for creative or LP issues. **Adoption** protects against “hollow” growth: installs that never touch the product rarely become paid. **Time-to-install** and the **no-install retargeting list** connect analytics to paid and lifecycle workflows.

---

*Last updated: aligned with `task2_analytics` Streamlit build and `grammarly_campaign_data.xlsx` schema.*
