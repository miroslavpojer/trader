"""
Phase 001: Read universe (tickers + source paths), extract **daily price** per ticker,
and save one parquet per ticker:  data/001_raw_data/<TICKER>.parquet

Heuristics:
- look for .parquet/.csv files under provided globs that contain 'price'/'ohlcv'/'bars' in filename;
  fallback to any parquet/csv if none match.
- normalize columns to ['ticker','date','open','high','low','close','volume']
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict, List
import pandas as pd

REQUIRED = ["ticker","date","open","high","low","close","volume"]

def universe_list(cfg: Dict) -> list[str]:
    return list(cfg.get("universe",{}).get("tickers", []))

def phase_dir(cfg: Dict, phase: str) -> Path:
    base = Path(cfg.get("io",{}).get("phase_dir","data"))
    d = base / phase
    d.mkdir(parents=True, exist_ok=True)
    return d

def find_price_files_for_ticker(cfg: Dict, ticker: str) -> List[Path]:
    patterns = [p.format(ticker=ticker) for p in cfg.get("universe",{}).get("sources",[])]
    found: List[Path] = []
    for pat in patterns:
        for f in Path().glob(pat):
            if not f.is_file():
                continue
            low = f.name.lower()
            if any(k in low for k in ("price","ohlcv","bars","quotes")) and f.suffix.lower() in (".parquet",".pq",".csv"):
                found.append(f)
    if not found:
        for pat in patterns:
            for f in Path().glob(pat):
                if f.is_file() and f.suffix.lower() in (".parquet",".pq",".csv"):
                    found.append(f)
    return found

def load_daily_price_from_file(path: Path) -> pd.DataFrame:
    if path.suffix.lower() == ".csv":
        df = pd.read_csv(path)
    else:
        df = pd.read_parquet(path)
    # naive normalization
    out = pd.DataFrame()
    for k in REQUIRED:
        cand = None
        for c in df.columns:
            if c.lower() == k:
                cand = c; break
        if cand is None and k == "date":
            for c in df.columns:
                if c.lower() in ("datetime","timestamp","time","date"):
                    cand = c; break
        out[k] = df[cand] if cand else pd.Series([pd.NA]*len(df))
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    out = out.dropna(subset=["date","close"])
    if "ticker" in out and out["ticker"].isna().any():
        out["ticker"] = out["ticker"].fillna(method="ffill").fillna(method="bfill")
    return out[REQUIRED]

def collect_ticker(cfg: Dict, ticker: str) -> Path:
    files = find_price_files_for_ticker(cfg, ticker)
    if not files:
        raise FileNotFoundError(f"No price-like files for {ticker}")
    dfs = [load_daily_price_from_file(p) for p in files]
    df = pd.concat(dfs, ignore_index=True)
    df = df.sort_values("date").drop_duplicates(subset=["date"])
    df["ticker"] = ticker
    out_dir = phase_dir(cfg, "001_raw_data")
    out_path = out_dir / f"{ticker}.parquet"
    df.to_parquet(out_path, index=False)
    return out_path

def run_phase_001_collect(cfg: Dict) -> list[Path]:
    tickers = universe_list(cfg)
    outs = []
    for t in tickers:
        try:
            outs.append(collect_ticker(cfg, t))
        except Exception as e:
            print(f"[WARN] {t}: {e}")
    return outs
