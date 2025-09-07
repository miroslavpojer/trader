import pandas as pd
import numpy as np
import pytest

@pytest.fixture
def synthetic_raw_df():
    data = {
        "ticker": ["AAA"]*10 + ["BBB"]*10,
        "date": pd.date_range("2024-01-01", periods=10, freq="D").tolist()
                + pd.date_range("2024-01-01", periods=10, freq="D").tolist(),
        "open": np.linspace(100, 110, 20),
        "high": np.linspace(101, 111, 20),
        "low":  np.linspace(99, 109, 20),
        "close": np.linspace(100, 110, 20),
        "volume": [1000]*20
    }
    return pd.DataFrame(data)
