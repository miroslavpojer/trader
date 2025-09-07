from trader.utils.clean import sanitize, check_ranges

def test_sanitize_and_ranges(synthetic_raw_df):
    df = sanitize(synthetic_raw_df.copy())
    check_ranges(df)  # should not raise
