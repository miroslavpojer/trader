"""Utility helpers."""
from __future__ import annotations
from pathlib import Path
import pandas as pd

def save_parquet_if_needed(df: pd.DataFrame, path: str):
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(path, index=False)
