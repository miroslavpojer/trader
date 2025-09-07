"""Common signal helpers (quality filters, breakout)."""
from __future__ import annotations
import pandas as pd

def quality_filters(df: pd.DataFrame, hurst_col="hurst_price_250", hurst_max=0.45,
                    atrp_col="atrp_14", atrp_range=(0.01,0.04), event_col="event_block"):
    """Return DataFrame with 'eligible' = 1 if passes filters (Hurst + ATR% + no events)."""
    cond = (df[hurst_col] <= hurst_max) & (df[atrp_col].between(atrp_range[0], atrp_range[1], inclusive="both"))
    if event_col in df.columns:
        cond &= (df[event_col] != 1)
    df["eligible"] = cond.astype(int)
    return df

def detect_breakout(df: pd.DataFrame, lookback=20, out="breakout_up"):
    """Simple breakout flag if today's high > rolling max(high, lookback-1)."""
    rollmax = df.groupby("ticker")["high"].transform(lambda s: s.shift(1).rolling(lookback-1, min_periods=3).max())
    df[out] = (df["high"] > rollmax).astype(int)
    return df
