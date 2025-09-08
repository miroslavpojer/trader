"""Base Strategy with phases 002/003/004 per ticker."""
from __future__ import annotations
from pathlib import Path
import pandas as pd
from typing import Tuple

class StrategyBase:
    name = "base"
    def __init__(self, cfg: dict):
        self.cfg = cfg
        self.phase_dir = Path(cfg.get("io",{}).get("phase_dir","data"))

    def phase002_path(self) -> Path:
        d = self.phase_dir / f"002_{self.name}_augmentation"; d.mkdir(parents=True, exist_ok=True); return d
    def phase003_path(self) -> Path:
        d = self.phase_dir / f"003_{self.name}_signal"; d.mkdir(parents=True, exist_ok=True); return d
    def phase004_path(self) -> Path:
        d = self.phase_dir / f"004_{self.name}_backtest"; d.mkdir(parents=True, exist_ok=True); return d

    def augment(self, df: pd.DataFrame, params: dict) -> pd.DataFrame: raise NotImplementedError
    def signals(self, df: pd.DataFrame, params: dict) -> pd.DataFrame: raise NotImplementedError
    def backtest(self, df: pd.DataFrame, params: dict, risk: dict) -> Tuple[pd.DataFrame, pd.DataFrame, dict]: raise NotImplementedError

    def run_for_ticker(self, ticker: str, params: dict, risk: dict):
        raw_path = self.phase_dir / "001_raw_data" / f"{ticker}.parquet"
        if not raw_path.exists():
            raise FileNotFoundError(f"Missing 001 parquet for {ticker}: {raw_path}")
        df = pd.read_parquet(raw_path)

        df_aug = self.augment(df, params)
        (self.phase002_path() / f"{ticker}.parquet").write_bytes(df_aug.to_parquet(index=False))

        df_sig = self.signals(df_aug, params)
        (self.phase003_path() / f"{ticker}.parquet").write_bytes(df_sig.to_parquet(index=False))

        trades, equity, summary = self.backtest(df_sig, params, risk)
        out4 = self.phase004_path()
        trades.to_csv(out4 / f"{ticker}_trades.csv", index=False)
        equity.to_csv(out4 / f"{ticker}_equity.csv", index=False)
        import pandas as pd
        pd.Series(summary).to_csv(out4 / f"{ticker}_summary.json")
        return trades, equity, summary
