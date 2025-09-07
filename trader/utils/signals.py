"""Signal generation & filters."""
from __future__ import annotations
import pandas as pd

def apply_quality_filters(df: pd.DataFrame, hurst_col: str = "hurst_price_250", hurst_max: float = 0.45,
                          atrp_col: str = "atrp_14", atrp_range=(0.01,0.04), event_col: str = "event_block") -> pd.DataFrame:
    """Create 'eligible' flag combining Hurst, ATR% band, and optional event block."""
    cond = (df[hurst_col] <= hurst_max) & (df[atrp_col].between(atrp_range[0], atrp_range[1], inclusive="both"))
    if event_col in df.columns:
        cond &= (df[event_col] != 1)
    df["eligible"] = cond.astype(int)
    return df

def generate_long_signals(df: pd.DataFrame, z_col: str = "z_ema20_20",
                          z_entry: float = -2.5, z_exit: float = -0.5,
                          stop_z: float = -3.5, time_stop: int = 5,
                          eligible_col: str = "eligible") -> pd.DataFrame:
    """Produce long MR signals and attach trade parameters."""
    df["signal_long"] = ((df[z_col] <= z_entry) & (df[eligible_col] == 1)).astype(int)
    df["entry_z"] = z_entry
    df["exit_z"] = z_exit
    df["stop_z"] = stop_z
    df["time_stop_bars"] = int(time_stop)
    return df
