"""QuietFlow (ETF Rotation) pipeline.

Měsíční rotace do top-N ETF podle 3–6M momentum, vážení inverse volatility.
"""
from __future__ import annotations
import pandas as pd
import numpy as np
from pathlib import Path

def compute_momentum(df: pd.DataFrame, months: int, out: str):
    """Price momentum = close / close.shift(LB) - 1 (approx)."""
    lb = int(months*21)
    df[out] = df.groupby("ticker")["close"].transform(lambda s: s / s.shift(lb) - 1.0)
    return df

def compute_vola(df: pd.DataFrame, window: int, out: str):
    df[out] = df.groupby("ticker")["close"].transform(lambda s: s.pct_change().rolling(window).std())
    return df

def monthly_rotation(df: pd.DataFrame, top_n: int, vola_col: str, mom_cols: list[str]):
    """Naivní monthly pick top-N by (avg momentum) and inverse-vol weights.
    Returns DataFrame with 'weight' per ticker per month (placeholder)."""
    df["month"] = pd.to_datetime(df["date"]).dt.to_period("M")
    agg = df.groupby(["month","ticker"])[mom_cols+[vola_col]].last().reset_index()
    agg["mom_avg"] = agg[mom_cols].mean(axis=1)
    # rank & pick
    selections = []
    for m, g in agg.groupby("month"):
        top = g.sort_values("mom_avg", ascending=False).head(top_n).copy()
        inv_vol = 1.0 / top[vola_col].replace(0, np.nan)
        w = inv_vol / inv_vol.sum()
        top["weight"] = w.fillna(0.0)
        selections.append(top[["month","ticker","weight"]])
    sel = pd.concat(selections, ignore_index=True) if selections else pd.DataFrame(columns=["month","ticker","weight"])
    return sel

def run_pipeline(cfg: dict):
    """Compute ETF momentum/vola → monthly picks → export summary (placeholder backtest)."""
    base = cfg["cache"]["base_ohlcv"]
    df = pd.read_parquet(base)

    p = cfg["strategies"]["etf"]["params"]
    df = compute_momentum(df, months=int(p["momentum_lookback_m"][0]), out="mom_3m")
    df = compute_momentum(df, months=int(p["momentum_lookback_m"][1]), out="mom_6m")
    df = compute_vola(df, window=int(p["vola_lookback_d"]), out="vola_20")

    sel = monthly_rotation(df, top_n=int(p["top_n"]), vola_col="vola_20", mom_cols=["mom_3m","mom_6m"])

    # TODO: portfolio backtest (apply weights next month, hold for 1M)
    trades = pd.DataFrame(columns=["month","ticker","weight"])
    equity = pd.DataFrame(columns=["date","equity"])
    summary = {"Sharpe_vs_SPY": 0.0, "MaxDD": 0.0}

    out = Path("reports/etf"); out.mkdir(parents=True, exist_ok=True)
    sel.to_csv(out/"selection.csv", index=False)
    trades.to_csv(out/"trades.csv", index=False)
    equity.to_csv(out/"equity.csv", index=False)
    pd.Series(summary).to_csv(out/"summary.json")
