"""ETF Rotation (QuietFlow) pipeline (per-ticker augment; portfolio-level TODO)."""
from __future__ import annotations
import pandas as pd
from trader.strategies.base import StrategyBase

class ETFStrategy(StrategyBase):
    name = "etf"

    def augment(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        lb3 = int(21*params.get("momentum_lookback_m",[3,6])[0])
        lb6 = int(21*params.get("momentum_lookback_m",[3,6])[1])
        df["mom_3m"] = df.groupby("ticker")["close"].transform(lambda s: s / s.shift(lb3) - 1.0)
        df["mom_6m"] = df.groupby("ticker")["close"].transform(lambda s: s / s.shift(lb6) - 1.0)
        df["vola_20"] = df.groupby("ticker")["close"].transform(lambda s: s.pct_change().rolling(int(params.get("vola_lookback_d",20))).std())
        return df

    def signals(self, df: pd.DataFrame, params: dict) -> pd.DataFrame:
        df["score"] = df[["mom_3m","mom_6m"]].mean(axis=1) / (df["vola_20"].replace(0, pd.NA))
        return df

    def backtest(self, df: pd.DataFrame, params: dict, risk: dict):
        trades = pd.DataFrame(columns=["date","ticker","weight"])
        equity = pd.DataFrame(columns=["date","equity"])
        summary = {"Sharpe_vs_SPY": 0.0, "MaxDD": 0.0}
        return trades, equity, summary

def run_strategy(cfg: dict):
    tickers = cfg.get("universe",{}).get("tickers", [])
    params = cfg.get("strategies",{}).get("etf",{}).get("params", {})
    risk = cfg.get("strategies",{}).get("etf",{}).get("risk", {})
    strat = ETFStrategy(cfg)
    for t in tickers:
        try:
            strat.run_for_ticker(t, params, risk)
        except Exception as e:
            print(f"[ETF WARN] {t}: {e}")
