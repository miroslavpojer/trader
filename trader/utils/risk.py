"""Position sizing utilities."""
from __future__ import annotations
import pandas as pd
import numpy as np

def atr_volatility_sizing(df: pd.DataFrame, risk_perc: float = 0.01, atr_col: str = "atr_14",
                          price_col: str = "close", out_col: str = "position_size") -> pd.DataFrame:
    """Compute position size based on % account risk and ATR. Placeholder equity=100k."""
    equity = 100_000.0  # TODO: pass actual equity
    risk_amount = equity * risk_perc
    df[out_col] = risk_amount / df[atr_col].replace(0, np.nan)
    df[out_col] = df[out_col].fillna(0.0)
    return df
