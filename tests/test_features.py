from trader.utils.features import add_ema, add_residuals_zscore, add_atr, add_hurst, add_ou_halflife

def test_features_pipeline(synthetic_raw_df):
    df = add_ema(synthetic_raw_df.copy(), window=3)
    df = add_residuals_zscore(df, std_window=3)
    df = add_atr(df, window=3)
    df = add_hurst(df, window=5)
    df = add_ou_halflife(df, lookback=5)
    assert "ema_20" in df.columns
    assert "z_ema20_20" in df.columns
    assert "atr_14" in df.columns
    assert "hurst_price_250" in df.columns
    assert "ou_half_life" in df.columns
