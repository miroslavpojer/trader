"""Data cleaning & normalization."""
from __future__ import annotations
import pandas as pd

def sanitize(df: pd.DataFrame) -> pd.DataFrame:
    """Sort by ['ticker','date'], drop duplicates, drop rows with NaN in key price fields."""
    df = df.sort_values(["ticker","date"]).drop_duplicates()
    df = df.dropna(subset=["open","high","low","close","volume"])
    return df

def check_ranges(df: pd.DataFrame) -> None:
    """Basic range checks: price > 0, volume >= 0, high/low consistency."""
    if (df["close"] <= 0).any():
        raise ValueError("Found non-positive close price.")
    if (df["volume"] < 0).any():
        raise ValueError("Found negative volume.")
    if (df["high"] < df["low"]).any():
        raise ValueError("Found high < low.")

def adjust_prices_if_needed(df: pd.DataFrame, method: str = "none") -> pd.DataFrame:
    """Placeholder for split/dividend adjustments. Currently no-op unless implemented."""
    # TODO: implement or validate adjusted prices
    return df
