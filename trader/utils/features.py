"""Feature engineering functions."""
from __future__ import annotations
import pandas as pd
import numpy as np

def add_ema(df: pd.DataFrame, window: int = 20, price_col: str = "close", out_col: str = "ema_20") -> pd.DataFrame:
    """Compute EMA per ticker and append as column."""
    df[out_col] = df.groupby("ticker")[price_col].transform(lambda s: s.ewm(span=window, adjust=False).mean())
    return df

def add_residuals_zscore(df: pd.DataFrame, price_col: str = "close", fair_col: str = "ema_20",
                         std_window: int = 20, out_cols=("resid_ema20","sigma_resid_ema20_20","z_ema20_20")) -> pd.DataFrame:
    """Residuals (price - fair), rolling std of residuals, and Z-score."""
    resid_col, sig_col, z_col = out_cols
    df[resid_col] = df[price_col] - df[fair_col]
    df[sig_col] = df.groupby("ticker")[resid_col].transform(lambda s: s.rolling(std_window, min_periods=std_window//2).std())
    df[z_col] = df[resid_col] / df[sig_col]
    return df

def add_atr(df: pd.DataFrame, window: int = 14, out_cols=("atr_14","atrp_14")) -> pd.DataFrame:
    """Average True Range and ATR% per ticker."""
    atr_col, atrp_col = out_cols
    def _atr(g):
        close_prev = g["close"].shift(1)
        tr = pd.concat([g["high"]-g["low"], (g["high"]-close_prev).abs(), (g["low"]-close_prev).abs()], axis=1).max(axis=1)
        return tr.rolling(window, min_periods=window//2).mean()
    df[atr_col] = df.groupby("ticker", group_keys=False).apply(_atr).reset_index(level=0, drop=True)
    df[atrp_col] = df[atr_col] / df["close"]
    return df

def add_hurst(df: pd.DataFrame, window: int = 250, price_col: str = "close", out_col: str = "hurst_price_250") -> pd.DataFrame:
    """Simple rolling Hurst exponent via R/S (rough approximation)."""
    def hurst_rs(x):
        if len(x) < 10:
            return np.nan
        y = x - x.mean()
        z = y.cumsum()
        R = z.max() - z.min()
        S = y.std(ddof=1)
        return np.nan if S == 0 else np.log(R/S) / np.log(len(x))
    df[out_col] = df.groupby("ticker")[price_col].transform(lambda s: s.rolling(window).apply(hurst_rs, raw=False))
    return df

def add_ou_halflife(df: pd.DataFrame, resid_col: str = "resid_ema20", lookback: int = 60, out_col: str = "ou_half_life") -> pd.DataFrame:
    """OU half-life from AR(1) coefficient on residuals (naive rolling)."""
    def _phi_to_hl(phi):
        import numpy as np
        if pd.isna(phi) or phi <= 0 or phi >= 1:
            return np.nan
        return -np.log(2) / np.log(phi)
    def rolling_phi(s):
        import numpy as np
        x = s.values
        res = np.full_like(x, np.nan, dtype=float)
        for i in range(lookback, len(x)):
            y = x[i-lookback+1:i+1]
            X = x[i-lookback:i]
            if np.std(X) == 0:
                continue
            phi = float(np.dot(X, y) / np.dot(X, X))
            res[i] = _phi_to_hl(phi)
        return pd.Series(res, index=s.index)
    df[out_col] = df.groupby("ticker")[resid_col].apply(rolling_phi).reset_index(level=0, drop=True)
    return df
