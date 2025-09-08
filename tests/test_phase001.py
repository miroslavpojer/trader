from trader.shared.phase001_collect import phase_dir
def test_phase_dir_builds(tmp_path):
    from trader.shared.phase001_collect import phase_dir as _pd
    cfg = {"io":{"phase_dir": str(tmp_path)}}
    d = _pd(cfg, "001_raw_data")
    assert d.exists()
