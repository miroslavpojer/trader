from trader.utils.signals import apply_quality_filters, generate_long_signals

def test_signals_generation(synthetic_raw_df):
    df = synthetic_raw_df.copy()
    df["ema_20"] = df["close"]
    df["resid_ema20"] = 0.0
    df["sigma_resid_ema20_20"] = 1.0
    df["z_ema20_20"] = -3.0
    df["atr_14"] = 1.0
    df["atrp_14"] = 0.02
    df["hurst_price_250"] = 0.3
    df = apply_quality_filters(df)
    df = generate_long_signals(df)
    assert df["signal_long"].sum() > 0
