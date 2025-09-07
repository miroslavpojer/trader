"""
CLI pro orchestraci: RAW ingest + jednotlivé pipelines (MR, Trend, ETF).
Použití:
  python -m trader.cli --config config/config.example.yml run_all
"""
from __future__ import annotations
import argparse, yaml
from pathlib import Path

from trader.orchestrator import run_all, run_pipeline, run_ingest

def load_config(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="Path to YAML config")
    sub = p.add_subparsers(dest="cmd", required=True)

    sub.add_parser("run_all")
    sub.add_parser("run_ingest")
    sp = sub.add_parser("run_pipeline")
    sp.add_argument("--name", required=True, choices=["mr","tf","etf"])

    args = p.parse_args(argv)
    cfg = load_config(args.config)

    if args.cmd == "run_all":
        run_all(cfg)
    elif args.cmd == "run_ingest":
        run_ingest(cfg)
    elif args.cmd == "run_pipeline":
        run_pipeline(cfg, args.name)

if __name__ == "__main__":
    main()
