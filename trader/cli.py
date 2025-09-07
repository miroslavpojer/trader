"""
CLI orchestrátor pipeline.
Spuštění:
  python -m trader.cli --config config/config.example.yml run
"""
from __future__ import annotations
import argparse, yaml
from pathlib import Path
import pandas as pd

from trader.utils.data_ingest import load_raw, validate_raw_schema
from trader.utils.clean import sanitize, check_ranges, adjust_prices_if_needed
from trader.utils.features import (
    add_ema, add_residuals_zscore, add_atr, add_hurst, add_ou_halflife
)
from trader.utils.events import add_event_block
from trader.utils.signals import apply_quality_filters, generate_long_signals
from trader.utils.risk import atr_volatility_sizing
from trader.core.backtest import run_vector_backtest
from trader.core.eval import evaluate_trades

def load_config(path: str) -> dict:
    """Load YAML config from path."""
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def end_to_end(cfg: dict):
    """Run full pipeline end-to-end, save reports to reports/."""
    # Ingest & validate
    df = load_raw(cfg["data"]["raw_paths"], tz=cfg["data"].get("tz","UTC"))
    validate_raw_schema(df)
    df = sanitize(df)
    check_ranges(df)
    if not cfg["data"].get("adjusted_prices", False):
        df = adjust_prices_if_needed(df, method="none")  # TODO implement

    # Features
    df = add_ema(df, window=cfg["features"]["ema_window"])
    df = add_residuals_zscore(
        df, price_col="close", fair_col="ema_20", std_window=cfg["features"]["z_std_window"]
    )
    df = add_atr(df, window=cfg["features"]["atr_window"])
    df = add_hurst(df, window=cfg["features"]["hurst_window"])
    df = add_ou_halflife(df, lookback=cfg["features"]["ou_lookback"])

    # Events (optional)
    if cfg.get("events",{}).get("earnings_path") or cfg.get("events",{}).get("dividends_path"):
        # TODO: load external calendars and pass below
        df = add_event_block(df, earnings_df=None, dividends_df=None,
                             pre=cfg["events"].get("pre",1), post=cfg["events"].get("post",1))

    # Signals & filters
    df = apply_quality_filters(
        df,
        hurst_col="hurst_price_250",
        hurst_max=cfg["signals"]["hurst_max"],
        atrp_col="atrp_14",
        atrp_range=(cfg["signals"]["atrp_min"], cfg["signals"]["atrp_max"]),
        event_col="event_block"
    )
    df = generate_long_signals(
        df,
        z_col="z_ema20_20",
        z_entry=cfg["signals"]["z_entry"],
        z_exit=cfg["signals"]["z_exit"],
        stop_z=cfg["signals"]["stop_z"],
        time_stop=cfg["signals"]["time_stop"],
        eligible_col="eligible"
    )

    # Risk (optional)
    df = atr_volatility_sizing(
        df,
        risk_perc=cfg["risk"]["risk_per_trade"],
        atr_col="atr_14",
        price_col="close",
        out_col="position_size"
    )

    # Backtest
    trades, equity, summary = run_vector_backtest(
        df,
        signal_col="signal_long",
        z_col="z_ema20_20",
        exit_z_col="exit_z",
        stop_z_col="stop_z",
        time_stop_col="time_stop_bars",
        capital=cfg["risk"]["capital"],
        max_concurrent=cfg["risk"]["max_concurrent"]
    )

    # Eval & Report
    metrics = evaluate_trades(trades)
    print("Summary:", metrics)
    out = Path("reports"); out.mkdir(parents=True, exist_ok=True)
    trades.to_csv(out / "trades.csv", index=False)
    equity.to_csv(out / "equity.csv", index=False)
    pd.Series(metrics).to_csv(out / "summary.csv")

def main(argv=None):
    p = argparse.ArgumentParser()
    p.add_argument("--config", required=True, help="Path to YAML config")
    sub = p.add_subparsers(dest="cmd")

    sub.add_parser("run", help="Run end-to-end pipeline")
    sub.add_parser("features", help="Compute features only (TBD)")
    sub.add_parser("signals", help="Compute signals only (TBD)")
    sub.add_parser("backtest", help="Run backtest only (TBD)")

    args = p.parse_args(argv)
    cfg = load_config(args.config)
    # For now always run full pipeline; subcommands TBD (TODO)
    end_to_end(cfg)

if __name__ == "__main__":
    main()
