"""Orchestrátor: spustí ingest a následně pipelines.

TODO:
- Paralelizace (concurrent.futures / joblib / subprocess per pipeline)
- Režimová logika (kill-switch MR v trending trhu, apod.)
"""
from __future__ import annotations
from pathlib import Path
from typing import Dict

from trader.shared.ingest import load_raw
from trader.shared.cleaning import sanitize, check_ranges, adjust_prices_if_needed
from trader.shared.utils import save_parquet_if_needed
from trader.pipelines.mr_elastic_snapback import run_pipeline as run_mr
from trader.pipelines.tf_steady_stride import run_pipeline as run_tf
from trader.pipelines.etf_quietflow import run_pipeline as run_etf

def run_ingest(cfg: Dict):
    """Run RAW ingest + clean and cache the base parquet files."""
    df = load_raw(cfg["data"]["raw_paths"], tz=cfg["data"].get("tz","UTC"))
    df = sanitize(df); check_ranges(df)
    if not cfg["data"].get("adjusted_prices", False):
        df = adjust_prices_if_needed(df, method="none")
    save_parquet_if_needed(df, cfg["cache"]["base_ohlcv"])
    # TODO: attach events and save cfg["cache"]["events"]

def run_pipeline(cfg: Dict, name: str):
    """Run single pipeline by name."""
    if name == "mr":
        return run_mr(cfg)
    if name == "tf":
        return run_tf(cfg)
    if name == "etf":
        return run_etf(cfg)
    raise ValueError(f"Unknown pipeline: {name}")

def run_all(cfg: Dict):
    """Run ingest first, then all pipelines (sequential placeholder)."""
    run_ingest(cfg)
    run_mr(cfg)
    run_tf(cfg)
    run_etf(cfg)
