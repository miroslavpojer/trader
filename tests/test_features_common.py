from trader.shared.features_common import sma, ema, atr, rsi2, bollinger

def test_features_minimal_df():
    import pandas as pd
    df = pd.DataFrame({
        "ticker": ["AAA"]*5,
        "date": pd.date_range("2024-01-01", periods=5, freq="D"),
        "open": [1,2,3,4,5],
        "high": [2,3,4,5,6],
        "low": [1,1,2,3,4],
        "close": [1.5,2.5,3.5,4.5,5.5],
        "volume": [100]*5
    })
    df = sma(df); df = ema(df); df = atr(df); df = rsi2(df); df = bollinger(df)
    assert "sma_20" in df.columns and "ema_20" in df.columns
