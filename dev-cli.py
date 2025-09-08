"""
DEV CLI for phased, multi-threaded multi-strategy pipeline.

Phases:
- 00_raw: load & clean raw data
- 01_mr: mean reversion strategy
- 02_tf: trend following strategy
- 03_etf: ETF rotation strategy

python -m trader.dev-cli --config config/dev_pipeline.yml

"""
import argparse
import logging
import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List

import yaml

# ---- Pipeline runners (adapt imports to your project layout) ----
# 00_raw
from pipelines.p00_raw_data import run_pipeline as run_00_raw
# 01_mr
from pipelines.p01_mean_reversion import run_pipeline as run_01_mr
# 02_tf
from pipelines.p02_trend_following import run_pipeline as run_02_tf
# 03_etf
from pipelines.p03_etf_rotation import run_pipeline as run_03_etf
from utils.logging_config import setup_logging

PIPELINE_HANDLERS = {
    "00_raw": run_00_raw,
    "01_mr": run_01_mr,
    "02_tf": run_02_tf,
    "03_etf": run_03_etf
}

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def _validate_cfg(cfg: Dict) -> None:
    if "pipelines" not in cfg or not isinstance(cfg["pipelines"], dict):
        raise ValueError("Config must contain a 'pipelines' mapping.")

    # Warn on unknown pipeline keys (helps catch typos like '01-mr' vs '01_mr')
    unknown = [k for k in cfg["pipelines"].keys() if k not in PIPELINE_HANDLERS]
    if unknown:
        logging.getLogger(__name__).warning(
            "Unknown pipeline keys in config (no runner registered): %s", unknown
        )

def _enabled_pipelines(cfg: Dict) -> list[str]:
    """Return enabled pipeline keys in config order."""
    pipelines = cfg.get("pipelines", {})
    ordered = list(pipelines.keys())
    return [k for k in ordered if pipelines.get(k, {}).get("enabled", False)]


def _run_one(name: str, cfg: Dict) -> str:
    logger = logging.getLogger(f"pipeline.{name}")
    handler = PIPELINE_HANDLERS.get(name)
    if handler is None:
        raise ValueError(f"No handler registered for pipeline '{name}'")

    t0 = time.perf_counter()
    logger.info("Starting pipeline: %s", name)
    handler(cfg)
    dt = time.perf_counter() - t0
    logger.info("Finished pipeline: %s in %.2fs", name, dt)
    return name

def main(argv=None):
    setup_logging()
    logger = logging.getLogger(__name__)
    logger.info("Starting dev-cli - phased multi-strategy pipeline")

    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True)
    args = p.parse_args(argv)
    cfg = load_config(args.config)
    _validate_cfg(cfg)

    enabled = _enabled_pipelines(cfg)
    if not enabled:
        logger.warning("No pipelines enabled in config. Nothing to do.")
        return

    # Always run 00_raw first if enabled
    rest: List[str] = [x for x in enabled if x != "00_raw"]
    if "00_raw" in enabled:
        logger.info("Running sequential phase: 00_raw")
        _run_one("00_raw", cfg)

    # Optionally gate on scheduler flag
    if not cfg.get("scheduler", {}).get("run_after_collect", True):
        logger.info("run_after_collect = False → skipping parallel phases")
        return

    # Run remaining pipelines in parallel
    if not rest:
        logger.info("No additional pipelines enabled after 00_raw.")
        return

    max_workers = int(cfg.get("scheduler", {}).get("max_workers", len(rest)))
    logger.info("Launching parallel pipelines: %s (max_workers=%d)", rest, max_workers)

    ok, failed = [], []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs = {ex.submit(_run_one, name, cfg): name for name in rest}
        for fut in as_completed(futs):
            name = futs[fut]
            try:
                fut.result()
                ok.append(name)
                logger.info("[OK] %s finished", name)
            except Exception as e:
                failed.append(name)
                logger.exception("[ERR] %s failed: %s", name, e)

    # Summary
    logger.info("Parallel phase complete. OK: %s | Failed: %s", ok, failed)
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
