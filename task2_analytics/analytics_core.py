"""Campaign data transforms and KPI helpers for the Grammarly growth dashboard."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pandas as pd

DATA_PATH = Path(__file__).resolve().parent / "data" / "grammarly_campaign_data.xlsx"


def _parse_extra(raw: Any) -> dict:
    if raw is None or (isinstance(raw, float) and pd.isna(raw)):
        return {}
    if isinstance(raw, dict):
        return raw
    if isinstance(raw, str):
        raw = raw.strip()
        if not raw or raw == "{}":
            return {}
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {}
    return {}


def load_raw(path: Path | None = None) -> pd.DataFrame:
    path = path or DATA_PATH
    df = pd.read_excel(path)
    df["timestamp"] = pd.to_datetime(df["timestamp"], utc=False)
    df["date"] = df["timestamp"].dt.normalize()
    df["extra_obj"] = df["extra"].apply(_parse_extra)
    df["lp_name"] = df["extra_obj"].apply(lambda d: d.get("lp_name"))
    df["product_feature"] = df["extra_obj"].apply(lambda d: d.get("product_feature"))
    return df


def first_touch_lp(df: pd.DataFrame) -> pd.Series:
    clicks = df[df["action"] == "did_click_lp"].sort_values("timestamp")
    first = clicks.groupby("user_id").first()
    return first["lp_name"].rename("attributed_lp")


def daily_event_counts(df: pd.DataFrame) -> pd.DataFrame:
    out = (
        df[df["action"].isin(["did_click_lp", "did_install_grammarly"])]
        .groupby(["date", "action"])
        .size()
        .unstack(fill_value=0)
        .rename(
            columns={
                "did_click_lp": "clicks",
                "did_install_grammarly": "installs",
            }
        )
        .reset_index()
    )
    if "clicks" not in out.columns:
        out["clicks"] = 0
    if "installs" not in out.columns:
        out["installs"] = 0
    out["cvr"] = out.apply(
        lambda r: (r["installs"] / r["clicks"]) if r["clicks"] > 0 else 0.0, axis=1
    )
    return out.sort_values("date")


def campaign_tables(df: pd.DataFrame, user_lp: pd.Series) -> tuple[pd.DataFrame, pd.DataFrame]:
    c = df[df["action"] == "did_click_lp"]
    click_by_lp = c.groupby("lp_name")["user_id"].nunique().rename("unique_clickers")

    installers = set(df.loc[df["action"] == "did_install_grammarly", "user_id"])
    inst_by_lp = user_lp[user_lp.index.isin(installers)].value_counts()
    inst_by_lp = inst_by_lp.reindex(click_by_lp.index, fill_value=0).rename("installs_attributed")

    summary = (
        pd.DataFrame({"unique_clickers": click_by_lp, "installs_attributed": inst_by_lp})
        .reset_index()
    )
    summary["cvr"] = summary.apply(
        lambda r: r["installs_attributed"] / r["unique_clickers"]
        if r["unique_clickers"] > 0
        else 0.0,
        axis=1,
    )

    click_events = c.groupby("lp_name").size().rename("click_events").reset_index()
    stacked = click_events.merge(
        summary[["lp_name", "installs_attributed"]].rename(
            columns={"installs_attributed": "install_users_attributed"}
        ),
        on="lp_name",
        how="left",
    ).fillna({"install_users_attributed": 0})
    return summary, stacked


def try_feature_counts(df: pd.DataFrame) -> pd.DataFrame:
    t = df[df["action"] == "try_grammarly"]
    return (
        t.groupby("product_feature")
        .size()
        .reset_index(name="try_events")
        .sort_values("try_events", ascending=True)
    )


def funnel_counts(df: pd.DataFrame) -> dict[str, int]:
    click_u = df.loc[df["action"] == "did_click_lp", "user_id"].nunique()
    inst_u = df.loc[df["action"] == "did_install_grammarly", "user_id"].nunique()
    try_u = df.loc[df["action"] == "try_grammarly", "user_id"].nunique()
    return {"clicked": click_u, "installed": inst_u, "tried": try_u}


def time_to_install_seconds(df: pd.DataFrame) -> pd.Series:
    clicks = df[df["action"] == "did_click_lp"].groupby("user_id")["timestamp"].min()
    inst = df[df["action"] == "did_install_grammarly"].groupby("user_id")["timestamp"].min()
    common = clicks.index.intersection(inst.index)
    delta = inst.loc[common] - clicks.loc[common]
    return delta.dt.total_seconds()


def retargeting_no_install(df: pd.DataFrame) -> pd.DataFrame:
    clickers = set(df.loc[df["action"] == "did_click_lp", "user_id"])
    installed = set(df.loc[df["action"] == "did_install_grammarly", "user_id"])
    cand = clickers - installed
    c = df[df["action"] == "did_click_lp"]
    first = c[c["user_id"].isin(cand)].sort_values("timestamp").groupby("user_id").first()
    return (
        first.reset_index()[["user_id", "lp_name", "timestamp"]]
        .rename(columns={"timestamp": "first_click_at"})
        .sort_values("first_click_at", ascending=False)
    )
