from trader.core.backtest import run_vector_backtest

def test_backtest_placeholder_runs(synthetic_raw_df):
    df = synthetic_raw_df.copy()
    df["z_ema20_20"] = -3.0
    df["eligible"] = 1
    df["signal_long"] = 1
    df["exit_z"] = -0.5
    df["stop_z"] = -3.5
    df["time_stop_bars"] = 5
    trades, equity, summary = run_vector_backtest(df)
    assert isinstance(summary, dict)
