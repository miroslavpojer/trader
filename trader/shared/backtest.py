"""Vector backtest (placeholder)."""
from __future__ import annotations
import pandas as pd

def run_vector_backtest(df: pd.DataFrame,
                        signal_col="signal_long",
                        exit_rules: dict | None = None) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Run toy vector backtest. Returns (trades, equity, summary)."""
    # TODO: implement TP/SL/TIME, concurrency, cash/equity accounting
    trades = pd.DataFrame(columns=["ticker","entry_date","entry_px","exit_date","exit_px","qty","pnl","return","bars_held"])
    equity = pd.DataFrame(columns=["date","equity","cash","exposure"])
    summary = {"WR": 0.0, "PF": 0.0, "Sharpe": 0.0, "MaxDD": 0.0}
    return trades, equity, summary
