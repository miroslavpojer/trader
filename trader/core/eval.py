"""Evaluation utilities for backtest outputs."""
from __future__ import annotations
import pandas as pd

def evaluate_trades(trades: pd.DataFrame) -> dict:
    """Compute WR, PF, avg win/loss, expectancy, max DD (placeholder)."""
    if trades.empty:
        return {"WR": 0.0, "PF": 0.0, "AvgWin": 0.0, "AvgLoss": 0.0, "Expectancy": 0.0, "MaxDD": 0.0, "Sharpe": 0.0}
    # TODO: real implementation
    return {"WR": 0.5, "PF": 1.1, "AvgWin": 1.0, "AvgLoss": -0.9, "Expectancy": 0.1, "MaxDD": 0.0, "Sharpe": 0.0}
