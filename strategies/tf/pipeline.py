"""Trend Following (SteadyStride) pipeline."""
from __future__ import annotations
import pandas as pd
from trader.strategies.base import StrategyBase
from trader.shared.features_common import sma, atr, adx
from trader.shared.signals_common import detect_breakout
from trader.shared.risk import atr_sizing
from trader.shared.backtest import run_vector_backtest
from trader.shared.eval import evaluate_trades

class TFStrategy(StrategyBase):
    name = "tf"

    def augment(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        df = sma(df, window=int(params.get("sma_fast",50)), out=f"sma_{int(params.get('sma_fast',50))}")
        df = sma(df, window=int(params.get("sma_slow",200)), out=f"sma_{int(params.get('sma_slow',200))}")
        df = atr(df, window=14)
        df = adx(df, window=14)  # placeholder
        return df

    def signals(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        df = detect_breakout(df, lookback=20, out="breakout_up")
        fast = f"sma_{int(params.get('sma_fast',50))}"
        slow = f"sma_{int(params.get('sma_slow',200))}"
        df["trend_on"] = ((df[fast] > df[slow]) & (df["adx_14"] >= float(params.get("adx_min",25)))).astype(int)
        df["signal_long"] = ((df["breakout_up"]==1) & (df["trend_on"]==1)).astype(int)
        return df

    def backtest(self, df: pd.DataFrame, params: dict, risk: dict):
        df = atr_sizing(df, risk_perc=float(risk.get("risk_per_trade", 0.01)))
        trades, equity, _summary = run_vector_backtest(df, signal_col="signal_long", exit_rules={"atr_trail_k": float(params.get("atr_trail_k",2.0))})
        metrics = evaluate_trades(trades)
        return trades, equity, metrics

def run_strategy(cfg: dict):
    tickers = cfg.get("universe",{}).get("tickers", [])
    params = cfg.get("strategies",{}).get("tf",{}).get("params", {})
    risk = cfg.get("strategies",{}).get("tf",{}).get("risk", {})
    strat = TFStrategy(cfg)
    for t in tickers:
        try:
            strat.run_for_ticker(t, params, risk)
        except Exception as e:
            print(f"[TF WARN] {t}: {e}")
