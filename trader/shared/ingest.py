"""RAW ingest & schema validation."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Sequence

REQUIRED = ["ticker","date","open","high","low","close","volume"]

def load_raw(paths: Sequence[str], tz: str = "UTC") -> pd.DataFrame:
    """Load last ~1y OHLCV from CSV/Parquet globs.
    TODO:
      - Normalize dtypes (category ticker, datetime tz-aware)
      - Filtering last 365 days
      - Support for reading Parquet fastpath
    Returns
    -------
    DataFrame with at least REQUIRED columns.
    """
    files = []
    for pat in paths:
        files.extend(Path().glob(pat))
    if not files:
        raise FileNotFoundError(f"No files matched patterns: {paths}")
    dfs = []
    for f in files:
        if f.suffix.lower() == ".csv":
            dfs.append(pd.read_csv(f))
        elif f.suffix.lower() in [".parquet", ".pq"]:
            dfs.append(pd.read_parquet(f))
        else:
            raise ValueError(f"Unsupported file type: {f}")
    df = pd.concat(dfs, ignore_index=True)
    return df
