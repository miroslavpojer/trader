"""SteadyStride (Trend Following) pipeline.

BUY:
  - Breakout (nové swing high / nad lokální rezistencí)
  - Cena nad SMA50 a SMA200
  - Exit: trailing stop (2*ATR) nebo návrat pod SMA50
"""
from __future__ import annotations

import logging

import pandas as pd
from pathlib import Path

logger = logging.getLogger(__name__)

def run_pipeline(cfg: dict):
    logger.debug("Running trend following pipeline with config: %s", cfg)
    # """Compute features → breakout signals → risk → backtest → export reports for Trend Following."""
    # base = cfg["cache"]["base_ohlcv"]
    # df = pd.read_parquet(base)
    #
    # p = cfg["strategies"]["tf"]["params"]
    # # Features
    # df = sma(df, window=p["sma_fast"], out=f"sma_{p['sma_fast']}")
    # df = sma(df, window=p["sma_slow"], out=f"sma_{p['sma_slow']}")
    # df = atr(df, window=14, out_atr="atr_14", out_atrp="atrp_14")
    # df = adx(df, window=14, out="adx_14")  # placeholder
    #
    # # Breakout & trend filter
    # df = detect_breakout(df, lookback=20, out="breakout_up")
    # df["trend_on"] = ((df[f"sma_{p['sma_fast']}"] > df[f"sma_{p['sma_slow']}"]) & (df["adx_14"] >= p["adx_min"])).astype(int)
    # df["signal_long"] = ((df["breakout_up"]==1) & (df["trend_on"]==1)).astype(int)
    #
    # # Risk
    # r = cfg["strategies"]["tf"]["risk"]
    # df = atr_sizing(df, risk_perc=r["risk_per_trade"], atr_col="atr_14", out="position_size", equity=100_000.0)
    #
    # # Backtest (placeholder)
    # trades, equity, summary = run_vector_backtest(df, signal_col="signal_long", exit_rules={"atr_trail_k": p["atr_trail_k"]})
    #
    # # Eval & export
    # metrics = evaluate_trades(trades)
    # out = Path("reports/tf"); out.mkdir(parents=True, exist_ok=True)
    # trades.to_csv(out/"trades.csv", index=False)
    # equity.to_csv(out/"equity.csv", index=False)
    # pd.Series(metrics).to_csv(out/"summary.json")
