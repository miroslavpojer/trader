"""Elastic Snapback (Mean Reversion) pipeline.

BUY:
  - Hurst < 0.45
  - Close < lower Bollinger(20, 2σ)
  - Z-score < -2.0
  - RSI(2) < 5
  - Stop: swing low - 0.7*ATR(14)
  - Exit: SMA20 or RSI(2) > 70

SELL (symetricky pro mean reversion long/short, ale MVP je long-only):
  - Hurst < 0.45
  - Close > upper Bollinger(20, 2σ)
  - Z-score > +2.0
  - RSI(2) > 95
"""
from __future__ import annotations
import pandas as pd
from pathlib import Path
from trader.shared.features_common import ema, bollinger, atr, rsi2, hurst_rs_window
from trader.shared.features_common import ou_half_life
from trader.shared.signals_common import quality_filters
from trader.shared.risk import atr_sizing
from trader.shared.backtest import run_vector_backtest
from trader.shared.eval import evaluate_trades

def run_pipeline(cfg: dict):
    """Compute features → signals → risk → backtest → export reports for MR."""
    base = cfg["cache"]["base_ohlcv"]
    df = pd.read_parquet(base)

    # Features
    df = ema(df, span=20, out="ema_20")
    df["resid_ema20"] = df["close"] - df["ema_20"]
    df = bollinger(df, col="close", window=20, z=2.0, out_mid="bb_mid", out_low="bb_low", out_high="bb_high")
    df = atr(df, window=14, out_atr="atr_14", out_atrp="atrp_14")
    df = rsi2(df, col="close", out="rsi2")
    df = hurst_rs_window(df, col="close", window=250, out="hurst_price_250")
    df = ou_half_life(df, resid_col="resid_ema20", lookback=60, out="ou_half_life")

    # Quality filters
    p = cfg["strategies"]["mr"]["params"]
    df = quality_filters(df, hurst_max=p["hurst_max"], atrp_range=(0.01,0.04))

    # Signals (long-only)
    df["signal_long"] = ((df["close"] < df["bb_low"]) & (df["rsi2"] < p["rsi2_buy_lt"]) & (df["eligible"]==1)).astype(int)

    # Risk sizing
    r = cfg["strategies"]["mr"]["risk"]
    df = atr_sizing(df, risk_perc=r["risk_per_trade"], atr_col="atr_14", out="position_size", equity=100_000.0)

    # Backtest (placeholder)
    trades, equity, summary = run_vector_backtest(df, signal_col="signal_long", exit_rules={"time_stop": p["time_stop"]})

    # Eval & export
    metrics = evaluate_trades(trades)
    out = Path("reports/mr"); out.mkdir(parents=True, exist_ok=True)
    trades.to_csv(out/"trades.csv", index=False)
    equity.to_csv(out/"equity.csv", index=False)
    pd.Series(metrics).to_csv(out/"summary.json")
