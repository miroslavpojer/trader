"""Risk sizing helpers."""
from __future__ import annotations
import pandas as pd
import numpy as np

def atr_sizing(df: pd.DataFrame, risk_perc=0.01, atr_col="atr_14", out="position_size", equity=100_000.0):
    """Position size ≈ risk_amount / ATR. TODO: hook actual equity from portfolio."""
    risk_amount = equity * float(risk_perc)
    df[out] = risk_amount / df[atr_col].replace(0, np.nan)
    df[out] = df[out].fillna(0.0)
    return df
