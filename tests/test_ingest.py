from trader.shared.ingest import load_raw
import pytest

def test_ingest_no_files_raises():
    with pytest.raises(FileNotFoundError):
        load_raw(paths=["./definitely/not/found/*.csv"])
