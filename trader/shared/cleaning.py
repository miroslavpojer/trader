"""Cleaning & basic validation."""
from __future__ import annotations
import pandas as pd

def sanitize(df: pd.DataFrame) -> pd.DataFrame:
    """Sort, drop duplicates, drop NaNs on key price fields."""
    df = df.sort_values(["ticker","date"]).drop_duplicates()
    df = df.dropna(subset=["open","high","low","close","volume"])
    return df

def check_ranges(df: pd.DataFrame) -> None:
    """Basic sanity: price>0, vol>=0, high>=low; raise on violation."""
    if (df["close"] <= 0).any():
        raise ValueError("Found non-positive close price.")
    if (df["volume"] < 0).any():
        raise ValueError("Found negative volume.")
    if (df["high"] < df["low"]).any():
        raise ValueError("Found high < low.")

def adjust_prices_if_needed(df: pd.DataFrame, method: str = "none") -> pd.DataFrame:
    """Placeholder for split/div adjustments (no-op by default)."""
    # TODO: implement split/div adjustment or verify adjusted inputs
    return df
