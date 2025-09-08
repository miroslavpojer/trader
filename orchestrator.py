"""
Orchestrator:
- Phase 001: collect per-ticker raw daily prices → parquet
- Then per strategy in parallel:
  - 002_strategy_augmentation
  - 003_strategy_signal
  - 004_strategy_backtest
"""
from __future__ import annotations
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List
from trader.shared.phase001_collect import run_phase_001_collect
from trader.strategies.mr.pipeline import run_strategy as run_mr
from trader.strategies.tf.pipeline import run_strategy as run_tf
from trader.strategies.etf.pipeline import run_strategy as run_etf

def run_phase_001(cfg: Dict):
    return run_phase_001_collect(cfg)

def _enabled(cfg: Dict) -> List[str]:
    names = []
    for n in ("mr","tf","etf"):
        if cfg.get("strategies",{}).get(n,{}).get("enabled", False):
            names.append(n)
    return names

def _run_one(cfg: Dict, name: str) -> str:
    if name == "mr":
        run_mr(cfg); return name
    if name == "tf":
        run_tf(cfg); return name
    if name == "etf":
        run_etf(cfg); return name
    raise ValueError(f"Unknown strategy: {name}")

def run_strategies_parallel(cfg: Dict):
    names = _enabled(cfg)
    if not names:
        return
    max_workers = int(cfg.get("scheduler",{}).get("max_workers", len(names)))
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = [ex.submit(_run_one, cfg, n) for n in names]
        for f in as_completed(futs):
            f.result()

def run_all(cfg: Dict):
    run_phase_001(cfg)
    if cfg.get("scheduler",{}).get("run_after_collect", True):
        run_strategies_parallel(cfg)
