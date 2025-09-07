from trader.core.eval import evaluate_trades
import pandas as pd

def test_eval_empty_trades():
    trades = pd.DataFrame()
    m = evaluate_trades(trades)
    assert "WR" in m and "PF" in m
