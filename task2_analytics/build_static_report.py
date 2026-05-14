#!/usr/bin/env python3
"""Build a standalone interactive HTML report for GitHub Pages (no server)."""

from __future__ import annotations

import html as html_lib
import re
import sys
from pathlib import Path

import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio

_ROOT = Path(__file__).resolve().parent
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

REPO_DOCS = _ROOT.parent / "docs"
OUT_HTML = REPO_DOCS / "campaign-dashboard.html"
SUMMARY_MD = _ROOT / "docs" / "reviewer_summary.md"


def _md_to_html_paragraphs(text: str) -> str:
    chunks = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    out = []
    for c in chunks:
        line = html_lib.escape(c)
        line = re.sub(r"\*\*(.+?)\*\*", lambda m: f"<strong>{m.group(1)}</strong>", line)
        out.append(f"<p>{line}</p>")
    return "\n".join(out)


def _fig_html(fig: go.Figure, *, include_plotlyjs: bool | str) -> str:
    return pio.to_html(
        fig,
        full_html=False,
        include_plotlyjs=include_plotlyjs,
        config={"displayModeBar": True, "responsive": True},
        default_width="100%",
    )


def main() -> None:
    df = load_raw()
    user_lp = first_touch_lp(df)
    daily = daily_event_counts(df)
    camp_sum, camp_stack = campaign_tables(df, user_lp)
    features = try_feature_counts(df)
    funnel = funnel_counts(df)
    tti = time_to_install_seconds(df)
    no_install = retargeting_no_install(df)

    uc, ui, ut = funnel["clicked"], funnel["installed"], funnel["tried"]
    user_cvr = ui / uc if uc else 0.0
    adopt = ut / ui if ui else 0.0

    summary_html = ""
    if SUMMARY_MD.is_file():
        summary_html = _md_to_html_paragraphs(SUMMARY_MD.read_text(encoding="utf-8"))

    # --- Figures (same logic as Streamlit app) ---
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

    fig1b = go.Figure(
        data=[
            go.Bar(
                x=daily["date"],
                y=100 * daily["cvr"],
                marker_color="#6366f1",
                name="Daily CVR (events)",
            )
        ]
    )
    fig1b.update_layout(
        height=280,
        yaxis_title="Installs ÷ clicks (%)",
        showlegend=False,
        margin=dict(t=48, b=48, l=48, r=32),
        title=dict(text="Daily CVR (event basis)", x=0.5, xanchor="center"),
    )

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
    fig2.update_layout(height=360, yaxis_title="User CVR (%)", title="Install rate by LP (first-touch)")

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
        title="Top product features tried",
    )

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
    fig3f.update_layout(height=320, margin=dict(t=20, b=20), title="User journey (unique users)")

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
                    color=["#0ea5e9", "#009e61", "#cbd5e1", "#7c3aed", "#94a3b8"],
                ),
                link=dict(
                    source=[0, 0, 1, 1],
                    target=[1, 2, 3, 4],
                    value=[funnel["installed"], dropped, funnel["tried"], dormant],
                ),
            )
        ]
    )
    fig4.update_layout(height=480, margin=dict(t=16, b=16, l=16, r=16), title="User-level funnel (Sankey)")

    fig4h = None
    med_txt = ""
    if len(tti) > 0:
        med = float(tti.median() / 60.0)
        med_txt = f"Median <strong>{med:.1f} min</strong> · n={len(tti):,} installers."
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
            title="Time from first LP click to install",
        )

    core_figs = [fig1, fig1b, fig2, fig2b, fig3, fig3f, fig4]
    pieces: list[str] = []
    first_js = True
    for fig in core_figs:
        pieces.append(_fig_html(fig, include_plotlyjs="cdn" if first_js else False))
        first_js = False

    hist_block = ""
    if fig4h is not None:
        hist_block = f'<p class="muted">{med_txt}</p>\n{_fig_html(fig4h, include_plotlyjs=False)}'

    camp_tbl = camp_sum.assign(cvr_pct=lambda d: (100 * d["cvr"]).round(2)).rename(
        columns={
            "lp_name": "Landing page",
            "unique_clickers": "Unique clickers",
            "installs_attributed": "Installs (attrib.)",
            "cvr_pct": "CVR %",
        }
    )

    ret = no_install.head(200)
    table_html = ret.to_html(index=False, classes="data", border=0, escape=True)

    caption_daily = ""
    if len(daily) >= 2:
        last, prev = daily.iloc[-1], daily.iloc[-2]
        if prev["clicks"] > 0 and last["clicks"] > 0:
            ddc = 100 * (last["cvr"] - prev["cvr"])
            d_last = pd.Timestamp(last["date"]).strftime("%b %d")
            caption_daily = (
                f"<p class=\"muted\">Latest day <strong>{d_last}</strong> (event-based): "
                f"{int(last['clicks']):,} clicks · {int(last['installs']):,} installs · "
                f"CVR <strong>{100 * last['cvr']:.1f}%</strong> ({ddc:+.1f} pts vs prior day).</p>"
            )

    full = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Grammarly campaigns — performance dashboard</title>
  <style>
    :root {{ font-family: "Segoe UI", system-ui, sans-serif; color: #0f172a; }}
    body {{ max-width: 1160px; margin: 0 auto; padding: 24px 20px 48px; line-height: 1.5; }}
    h1 {{ font-size: 1.75rem; margin: 0 0 0.25rem; }}
    .sub {{ color: #64748b; margin: 0 0 1.5rem; font-size: 1rem; }}
    .kpis {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(140px, 1fr)); gap: 12px; margin-bottom: 1.5rem; }}
    .kpi {{ background: #f8fafc; border: 1px solid #e2e8f0; border-radius: 10px; padding: 14px 16px; }}
    .kpi .v {{ font-size: 1.35rem; font-weight: 700; color: #009e61; }}
    .kpi .l {{ font-size: 0.8rem; color: #64748b; text-transform: uppercase; letter-spacing: 0.04em; }}
    section {{ margin-bottom: 2.5rem; }}
    h2 {{ font-size: 1.15rem; border-bottom: 1px solid #e2e8f0; padding-bottom: 8px; margin-top: 2rem; }}
    details {{ background: #f1f5f9; border-radius: 10px; padding: 12px 16px; margin-bottom: 1.5rem; }}
    details summary {{ cursor: pointer; font-weight: 600; }}
    .summary-body {{ margin-top: 12px; font-size: 0.95rem; }}
    .summary-body p {{ margin: 0 0 0.75rem; }}
    .muted {{ color: #64748b; font-size: 0.9rem; }}
    .js-plotly-plot {{ width: 100% !important; }}
    table.data {{ width: 100%; font-size: 0.88rem; border-collapse: collapse; margin: 12px 0; }}
    table.data th, table.data td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #e2e8f0; }}
    table.data th {{ background: #f8fafc; font-weight: 600; }}
    footer {{ margin-top: 3rem; font-size: 0.8rem; color: #94a3b8; }}
  </style>
</head>
<body>
  <h1>Grammarly multi-campaign performance</h1>
  <p class="sub">Interactive report — Task 2. Date range: {df["date"].min().date()} → {df["date"].max().date()} · {len(df):,} events.</p>

  <div class="kpis">
    <div class="kpi"><div class="l">Unique clickers</div><div class="v">{uc:,}</div></div>
    <div class="kpi"><div class="l">Installs</div><div class="v">{ui:,}</div></div>
    <div class="kpi"><div class="l">User CVR</div><div class="v">{100 * user_cvr:.1f}%</div></div>
    <div class="kpi"><div class="l">Trials (users)</div><div class="v">{ut:,}</div></div>
    <div class="kpi"><div class="l">Adoption</div><div class="v">{100 * adopt:.1f}%</div></div>
  </div>
  {caption_daily}

  <details>
    <summary>Why these metrics &amp; how success is measured (brief summary)</summary>
    <div class="summary-body">{summary_html}</div>
  </details>

  <p class="muted"><strong>Method:</strong> First-touch LP attribution (install rows have empty <code>extra</code>). CTR from ads requires impressions not in this extract.</p>

  <section><h2>1 · Daily overview</h2>{pieces[0]}{pieces[1]}</section>
  <section><h2>2 · Campaign comparison</h2>
    <div style="display:grid;grid-template-columns:1fr 1fr;gap:16px;align-items:start;">
      <div>{pieces[2]}</div>
      <div>{pieces[3]}</div>
    </div>
    <h3 style="font-size:1rem;margin-top:1rem;">Campaign table</h3>
    {camp_tbl.to_html(index=False, classes="data", border=0, escape=True)}
  </section>
  <section><h2>3 · Feature engagement</h2>
    <div style="display:grid;grid-template-columns:1.1fr 1fr;gap:16px;align-items:start;">
      <div>{pieces[4]}</div>
      <div>{pieces[5]}</div>
    </div>
  </section>
  <section><h2>4 · User funnel &amp; retargeting</h2>
    {pieces[6]}
    {hist_block}
    <h3 style="font-size:1rem;">Clicked but did not install ({len(no_install):,} users) — sample (first 200)</h3>
    {table_html}
    <p class="muted">For the full list, use the Streamlit app export or the project notebook.</p>
  </section>
  <footer>Static export · Plotly.js · Grammarly campaign exercise</footer>
</body>
</html>"""

    REPO_DOCS.mkdir(parents=True, exist_ok=True)
    OUT_HTML.write_text(full, encoding="utf-8")
    print(f"Wrote {OUT_HTML}")


if __name__ == "__main__":
    main()
