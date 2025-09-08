"""Vector backtest (placeholder).
TODO:
- first-hit TP/SL/TIME
- concurrency limit
- equity accounting
"""
from __future__ import annotations
import pandas as pd

def run_vector_backtest(df: pd.DataFrame, signal_col="signal_long", exit_rules=None):
    trades = pd.DataFrame(columns=["ticker","entry_date","entry_px","exit_date","exit_px","qty","pnl","return","bars_held"])
    equity = pd.DataFrame(columns=["date","equity","cash","exposure"])
    summary = {"WR": 0.0, "PF": 0.0, "Sharpe": 0.0, "MaxDD": 0.0}
    return trades, equity, summary
