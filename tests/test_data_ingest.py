from trader.utils.data_ingest import validate_raw_schema
import pandas as pd
import pytest

def test_validate_schema_missing_columns():
    df = pd.DataFrame({"ticker":["AAA"], "date":["2024-01-01"]})
    with pytest.raises(ValueError):
        validate_raw_schema(df)
