"""Streamlit dashboard: Grammarly campaign performance (Task 2 deliverable)."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

# Ensure local imports work when run as `streamlit run app.py`
_ROOT = Path(__file__).resolve().parent
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from analytics_core import (
    campaign_tables,
    daily_event_counts,
    first_touch_lp,
    funnel_counts,
    load_raw,
    retargeting_no_install,
    time_to_install_seconds,
    try_feature_counts,
)

st.set_page_config(
    page_title="Grammarly campaigns — performance",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.title("Grammarly multi-campaign performance")
st.caption(
    "Daily monitoring view: acquisition volume, LP comparison, post-install engagement, and funnel diagnostics."
)

_SUMMARY_PATH = _ROOT / "docs" / "reviewer_summary.md"
if _SUMMARY_PATH.is_file():
    with st.expander("Summary — why these metrics & what success means (brief for reviewers)", expanded=False):
        st.markdown(_SUMMARY_PATH.read_text(encoding="utf-8"))


@st.cache_data
def _load():
    return load_raw()


df = _load()
user_lp = first_touch_lp(df)
daily = daily_event_counts(df)
camp_sum, camp_stack = campaign_tables(df, user_lp)
features = try_feature_counts(df)
funnel = funnel_counts(df)
tti = time_to_install_seconds(df)
no_install = retargeting_no_install(df)

# ----- Sidebar -----
with st.sidebar:
    st.header("Scope")
    d0, d1 = df["date"].min(), df["date"].max()
    st.write(f"**Date range:** {d0.date()} → {d1.date()}")
    st.write(f"**Rows:** {len(df):,} events")
    st.markdown("---")
    st.subheader("Method notes")
    st.markdown(
        """
- **LP attribution:** first-touch `lp_name` on each user’s earliest `did_click_lp` carries through to install counts (install rows have empty `extra`).
- **CTR:** needs an impressions feed from ads; not in this extract—monitor **click volume** and CVR instead.
- **Campaign table:** users who clicked *both* LPs appear in both click cohorts; attributed install sits under their first LP only.
- **Written summary** (1–2 paragraphs): expander *Summary* at top of this page, or file `task2_analytics/docs/reviewer_summary.md` in the repo.
        """
    )

# ----- KPI strip (full width) -----
uc = funnel["clicked"]
ui = funnel["installed"]
ut = funnel["tried"]
user_cvr = ui / uc if uc else 0.0
adopt = ut / ui if ui else 0.0

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Unique clickers", f"{uc:,}")
c2.metric("Installs (users)", f"{ui:,}")
c3.metric("User CVR (install ÷ click)", f"{100 * user_cvr:.1f}%")
c4.metric("Feature trials (users)", f"{ut:,}")
c5.metric("Adoption (try ÷ install)", f"{100 * adopt:.1f}%")

if len(daily) >= 2:
    last = daily.iloc[-1]
    prev = daily.iloc[-2]
    d_last = pd.Timestamp(last["date"]).strftime("%b %d")
    ddc = (
        100 * (last["cvr"] - prev["cvr"])
        if prev["clicks"] > 0 and last["clicks"] > 0
        else 0.0
    )
    st.caption(
        f"Latest day **{d_last}** (event-based): {int(last['clicks']):,} clicks · "
        f"{int(last['installs']):,} installs · CVR **{100 * last['cvr']:.1f}%** "
        f"({ddc:+.1f} pts vs prior day)."
    )

tab1, tab2, tab3, tab4 = st.tabs(
    [
        "1 · Daily overview",
        "2 · Campaign comparison",
        "3 · Feature engagement",
        "4 · User funnel",
    ]
)

# --- Panel 1 ---
with tab1:
    st.subheader("Volume & event-level CVR")
    fig1 = go.Figure()
    fig1.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["clicks"],
            name="Clicks (LP)",
            mode="lines+markers",
            line=dict(color="#0ea5e9", width=2),
        )
    )
    fig1.add_trace(
        go.Scatter(
            x=daily["date"],
            y=daily["installs"],
            name="Installs",
            mode="lines+markers",
            line=dict(color="#009e61", width=2),
        )
    )
    fig1.update_layout(
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.22,
            x=0.5,
            xanchor="center",
        ),
        margin=dict(t=56, b=88, l=48, r=32),
        height=460,
        yaxis_title="Events",
        title=dict(text="Daily volume — clicks & installs", x=0.5, xanchor="center"),
    )
    st.plotly_chart(fig1, use_container_width=True)

    cvr_fig = go.Bar(
        x=daily["date"],
        y=100 * daily["cvr"],
        marker_color="#6366f1",
        name="Daily CVR (events)",
    )
    fig1b = go.Figure(data=[cvr_fig])
    fig1b.update_layout(
        height=280,
        yaxis_title="Installs ÷ clicks (%)",
        showlegend=False,
        margin=dict(t=48, b=48, l=48, r=32),
        title=dict(text="Daily CVR (event basis)", x=0.5, xanchor="center"),
    )
    st.plotly_chart(fig1b, use_container_width=True)
    st.caption(
        "Spikes or dips in daily CVR often trace to creative rotation, budget pacing, or tracking—compare with marketing calendar."
    )

# --- Panel 2 ---
with tab2:
    col_a, col_b = st.columns((1, 1))
    with col_a:
        st.markdown("##### Install rate by LP (first-touch)")
        fig2 = go.Figure(
            data=[
                go.Bar(
                    x=camp_sum["lp_name"],
                    y=100 * camp_sum["cvr"],
                    marker_color="#009e61",
                    text=[f"{100 * v:.1f}%" for v in camp_sum["cvr"]],
                    textposition="outside",
                )
            ]
        )
        fig2.update_layout(height=360, yaxis_title="User CVR (%)", xaxis_title="")
        st.plotly_chart(fig2, use_container_width=True)
    with col_b:
        st.markdown("##### Volume: click events vs attributed installs")
        fig2b = go.Figure(
            data=[
                go.Bar(
                    name="Click events",
                    x=camp_stack["lp_name"],
                    y=camp_stack["click_events"],
                    marker_color="#94a3b8",
                ),
                go.Bar(
                    name="Install users (attrib.)",
                    x=camp_stack["lp_name"],
                    y=camp_stack["install_users_attributed"],
                    marker_color="#009e61",
                ),
            ]
        )
        fig2b.update_layout(
            barmode="group",
            height=400,
            legend=dict(
                orientation="h",
                yanchor="top",
                y=-0.2,
                x=0.5,
                xanchor="center",
            ),
            margin=dict(t=52, b=80, l=48, r=32),
            yaxis_title="Count",
            title=dict(text="Volume — clicks vs attributed installs", x=0.5, xanchor="center"),
        )
        st.plotly_chart(fig2b, use_container_width=True)
    st.dataframe(
        camp_sum.assign(cvr_pct=lambda d: (100 * d["cvr"]).round(2)).rename(
            columns={
                "lp_name": "Landing page",
                "unique_clickers": "Unique clickers",
                "installs_attributed": "Installs (attrib.)",
                "cvr_pct": "CVR %",
            }
        ),
        use_container_width=True,
        hide_index=True,
    )

# --- Panel 3 ---
with tab3:
    st.subheader("Post-install product trials")
    fc1, fc2 = st.columns((1.1, 1))
    with fc1:
        fig3 = go.Figure(
            data=[
                go.Bar(
                    x=features["try_events"],
                    y=features["product_feature"],
                    orientation="h",
                    marker_color="#7c3aed",
                )
            ]
        )
        fig3.update_layout(
            height=280,
            xaxis_title="try_grammarly events",
            yaxis_title="",
            margin=dict(l=10),
        )
        st.plotly_chart(fig3, use_container_width=True)
    with fc2:
        st.markdown("##### User journey (unique users)")
        fig3f = go.Figure(
            data=[
                go.Funnel(
                    y=["Clicked LP", "Installed", "Tried a feature"],
                    x=[funnel["clicked"], funnel["installed"], funnel["tried"]],
                    textinfo="value+percent initial",
                    marker=dict(color=["#0ea5e9", "#009e61", "#7c3aed"]),
                )
            ]
        )
        fig3f.update_layout(height=320, margin=dict(t=20, b=20))
        st.plotly_chart(fig3f, use_container_width=True)
    st.caption(
        "Adoption rate = users with ≥1 `try_grammarly` ÷ installers. Low adoption after strong installs is an onboarding or product-discovery signal."
    )

# --- Panel 4 ---
with tab4:
    st.subheader("Funnel flow & retargeting inventory")
    dropped = funnel["clicked"] - funnel["installed"]
    dormant = funnel["installed"] - funnel["tried"]

    fig4 = go.Figure(
        data=[
            go.Sankey(
                arrangement="snap",
                node=dict(
                    pad=18,
                    thickness=22,
                    line=dict(color="rgba(0,0,0,0.12)", width=1),
                    label=[
                        "LP click",
                        "Installed",
                        "No install",
                        "Tried feature",
                        "Installed, no try",
                    ],
                    color=[
                        "#0ea5e9",
                        "#009e61",
                        "#cbd5e1",
                        "#7c3aed",
                        "#94a3b8",
                    ],
                ),
                link=dict(
                    source=[0, 0, 1, 1],
                    target=[1, 2, 3, 4],
                    value=[
                        funnel["installed"],
                        dropped,
                        funnel["tried"],
                        dormant,
                    ],
                ),
            )
        ]
    )
    fig4.update_layout(height=480, margin=dict(t=16, b=16, l=16, r=16))
    st.plotly_chart(fig4, use_container_width=True)

    st.markdown("##### Time from first LP click to install")
    if len(tti) > 0:
        med = tti.median() / 60.0
        st.caption(f"Median **{med:.1f} minutes** · n={len(tti):,} installers with a prior click.")
        tti_mins = tti / 60.0
        fig4h = go.Figure(
            data=[
                go.Histogram(
                    x=tti_mins.clip(upper=tti_mins.quantile(0.99)),
                    nbinsx=40,
                    marker_color="#009e61",
                )
            ]
        )
        fig4h.update_layout(
            height=260,
            xaxis_title="Minutes (winsorized at 99th pct)",
            yaxis_title="Users",
        )
        st.plotly_chart(fig4h, use_container_width=True)

    st.markdown(
        f"##### Clicked but did not install — **{len(no_install):,}** users (retargeting candidates)"
    )
    st.dataframe(
        no_install.head(500),
        use_container_width=True,
        hide_index=True,
        height=320,
    )
    if len(no_install) > 500:
        st.caption("Showing first 500 rows. Export from notebook or CSV if needed.")
    st.download_button(
        "Download retargeting list (CSV)",
        data=no_install.to_csv(index=False).encode("utf-8"),
        file_name="retargeting_click_no_install.csv",
        mime="text/csv",
    )
