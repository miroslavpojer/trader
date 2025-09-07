"""Common feature calculators (SMA/EMA/ATR/ADX/RSI, Hurst, OU)."""
from __future__ import annotations
import pandas as pd
import numpy as np

def sma(df: pd.DataFrame, col="close", window=20, out="sma_20"):
    df[out] = df.groupby("ticker")[col].transform(lambda s: s.rolling(window, min_periods=window//2).mean())
    return df

def ema(df: pd.DataFrame, col="close", span=20, out="ema_20"):
    df[out] = df.groupby("ticker")[col].transform(lambda s: s.ewm(span=span, adjust=False).mean())
    return df

def bollinger(df: pd.DataFrame, col="close", window=20, z=2.0, out_mid="bb_mid", out_low="bb_low", out_high="bb_high"):
    grp = df.groupby("ticker")[col]
    mid = grp.transform(lambda s: s.rolling(window, min_periods=window//2).mean())
    std = grp.transform(lambda s: s.rolling(window, min_periods=window//2).std())
    df[out_mid], df[out_low], df[out_high] = mid, mid - z*std, mid + z*std
    return df

def atr(df: pd.DataFrame, window=14, out_atr="atr_14", out_atrp="atrp_14"):
    def _atr(g):
        c1 = g["close"].shift(1)
        tr = pd.concat([g["high"]-g["low"], (g["high"]-c1).abs(), (g["low"]-c1).abs()], axis=1).max(axis=1)
        return tr.rolling(window, min_periods=window//2).mean()
    df[out_atr] = df.groupby("ticker", group_keys=False).apply(_atr).reset_index(level=0, drop=True)
    df[out_atrp] = df[out_atr] / df["close"]
    return df

def rsi2(df: pd.DataFrame, col="close", out="rsi2"):
    # naive 2-period RSI
    delta = df.groupby("ticker")[col].transform(lambda s: s.diff())
    up = delta.clip(lower=0.0).rolling(2).mean()
    down = (-delta.clip(upper=0.0)).rolling(2).mean()
    rs = up / (down.replace(0, np.nan))
    df[out] = 100.0 - (100.0 / (1.0 + rs))
    return df

def adx(df: pd.DataFrame, window=14, out="adx_14"):
    # placeholder ADX; TODO: replace with robust formula if needed
    df[out] = np.nan
    return df

def hurst_rs_window(df: pd.DataFrame, col="close", window=250, out="hurst_price_250"):
    def hurst_rs(x):
        if len(x) < 10:
            return np.nan
        y = x - x.mean()
        z = y.cumsum(); R = z.max() - z.min(); S = y.std(ddof=1)
        return np.nan if S == 0 else np.log(R/S) / np.log(len(x))
    df[out] = df.groupby("ticker")[col].transform(lambda s: s.rolling(window).apply(hurst_rs, raw=False))
    return df

def ou_half_life(df: pd.DataFrame, resid_col="resid_ema20", lookback=60, out="ou_half_life"):
    def _phi_to_hl(phi):
        if pd.isna(phi) or phi <= 0 or phi >= 1:
            return np.nan
        import numpy as np
        return -np.log(2) / np.log(phi)
    def rolling_phi(s):
        import numpy as np
        x = s.values
        res = np.full_like(x, np.nan, dtype=float)
        for i in range(lookback, len(x)):
            y = x[i-lookback+1:i+1]; X = x[i-lookback:i]
            if np.std(X) == 0:
                continue
            phi = float(np.dot(X, y) / np.dot(X, X))
            res[i] = _phi_to_hl(phi)
        return pd.Series(res, index=s.index)
    df[out] = df.groupby("ticker")[resid_col].apply(rolling_phi).reset_index(level=0, drop=True)
    return df
