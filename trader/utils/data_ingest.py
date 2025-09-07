"""Raw data ingest & schema validation."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Sequence

REQUIRED = ["ticker","date","open","high","low","close","volume"]

def load_raw(paths: Sequence[str], tz: str = "UTC") -> pd.DataFrame:
    """Load raw OHLCV files (CSV or Parquet) from given glob patterns.
    TODO:
    - support parquet/arrow
    - normalize dtypes
    - parse datetime with tz
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
    # TODO: dtype normalization + tz handling
    return df

def validate_raw_schema(df: pd.DataFrame, required=REQUIRED) -> None:
    """Raise ValueError if required columns missing or bad dtypes (TODO)."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")
    # TODO: dtype checks
