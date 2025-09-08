"""Mean Reversion (Elastic Snapback) pipeline."""
from __future__ import annotations
import pandas as pd
from trader.strategies.base import StrategyBase
from trader.shared.features_common import ema, bollinger, atr, rsi2, hurst_rs_window
from trader.shared.signals_common import quality_filters
from trader.shared.risk import atr_sizing
from trader.shared.backtest import run_vector_backtest
from trader.shared.eval import evaluate_trades

class MRStrategy(StrategyBase):
    name = "mr"

    def augment(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        df = ema(df, span=int(params.get("bb_window",20)), out="ema_20")
        df["resid_ema20"] = df["close"] - df["ema_20"]
        df = bollinger(df, col="close", window=int(params.get("bb_window",20)), z=float(params.get("bb_z",2.0)))
        df = atr(df, window=int(params.get("atr_window",14)))
        df = rsi2(df, col="close", out="rsi2")
        df = hurst_rs_window(df, col="close", window=250)
        return df

    def signals(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        df = quality_filters(df, hurst_max=float(params.get("hurst_max",0.45)), atrp_range=(0.01,0.04))
        df["signal_long"] = ((df["close"] < df["bb_low"]) & (df["rsi2"] < float(params.get("rsi2_buy_lt",5))) & (df["eligible"]==1)).astype(int)
        df["time_stop_bars"] = int(params.get("time_stop",5))
        return df

    def backtest(self, df: pd.DataFrame, params: dict, risk: dict):
        df = atr_sizing(df, risk_perc=float(risk.get("risk_per_trade", 0.01)))
        trades, equity, _summary = run_vector_backtest(df, signal_col="signal_long", exit_rules={"time_stop": int(params.get("time_stop",5))})
        metrics = evaluate_trades(trades)
        return trades, equity, metrics

def run_strategy(cfg: dict):
    tickers = cfg.get("universe",{}).get("tickers", [])
    params = cfg.get("strategies",{}).get("mr",{}).get("params", {})
    risk = cfg.get("strategies",{}).get("mr",{}).get("risk", {})
    strat = MRStrategy(cfg)
    for t in tickers:
        try:
            strat.run_for_ticker(t, params, risk)
        except Exception as e:
            print(f"[MR WARN] {t}: {e}")
