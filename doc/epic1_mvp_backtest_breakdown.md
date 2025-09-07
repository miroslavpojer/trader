# Epic 1 — MVP + Backtest (v3, Raw Input → Full Feature Pipeline)

Cíl: **plně zdokumentovaná Python pipeline**, která přebírá **syrová (raw) data** z těžby a v rámci pipeline provede:
1. Revizi dat (validace, čištění, normalizace)
2. Výpočet všech potřebných **features**
3. Generování **signálů**
4. **Risk/sizing**
5. **Backtest**
6. **Vyhodnocení výsledků**

> Fundamenty zůstávají **mimo** (použijí se při výběru universa mimo tuto pipeline). Pipeline ale umí volitelně připojit externí event kalendáře (earnings/dividendy) pro `event_block`.

---

## 0. Architektura & Tok dat

**Vstup:** syrové OHLCV (CSV/Parquet) z vytěženého zdroje, *bez* features.  
**Výstup:** report (metriky, equity), trade logy a (volitelně) export „feature‑ready“ datasetu.

### Kroky pipeline
1. **Load + Validate Raw** → `utils/data_ingest.py`
2. **Clean + Normalize** → `utils/clean.py`
3. **Feature Engineering** → `utils/features.py`
4. **Signals + Filters** → `utils/signals.py`
5. **Risk & Sizing** → `utils/risk.py`
6. **Backtest** → `core/backtest.py`
7. **Evaluation + Reports** → `core/eval.py` + `reports/`
8. **CLI Orchestrátor** → `cli.py`

---

## 1. Struktura repozitáře

```text
trader/
├─ cli.py
├─ config/
│  ├─ config.example.yml
│  └─ schemas/
├─ core/
│  ├─ backtest.py
│  └─ eval.py
├─ utils/
│  ├─ data_ingest.py
│  ├─ clean.py
│  ├─ features.py
│  ├─ signals.py
│  ├─ risk.py
│  ├─ events.py
│  └─ time_series.py
├─ reports/
├─ tests/
│  ├─ conftest.py
│  ├─ test_data_ingest.py
│  ├─ test_clean.py
│  ├─ test_features.py
│  ├─ test_signals.py
│  ├─ test_backtest.py
│  └─ test_eval.py
└─ README.md
```

---

## 2. Datové kontrakty (I/O)

### 2.1 RAW Input (požadované minimum)
- `["ticker","date","open","high","low","close","volume"]`
- Typy:
    - `ticker = str`
    - `date = datetime64` (nebo naive + `tz` v configu)
    - ceny = `float`
    - volume = `int/float`

### 2.2 Feature Output (po kroku 3)
- `ema_20`, `resid_ema20`, `sigma_resid_ema20_20`, `z_ema20_20`
- `atr_14`, `atrp_14`
- `hurst_price_250` **nebo** `hurst_resid_250`
- `ou_phi_resid`, `ou_half_life`
- `event_block` (0/1; pokud `events.py` použito)

### 2.3 Signals Output
- `eligible` (0/1)
- `signal_long` (0/1)
- `entry_z`, `exit_z`, `stop_z`, `time_stop_bars`
- *(volitelně)* `position_size`

### 2.4 Backtest Output
- **Trades:** `["ticker","entry_date","entry_px","exit_date","exit_px","qty","pnl","return","bars_held"]`
- **Equity:** `["date","equity","cash","exposure"]`
- **Summary:** dict/DF

---

## 3. API návrh (hlavní signatury)

### utils/data_ingest.py
- `load_raw(paths, tz="UTC")`: Načti syrové OHLCV (CSV/Parquet) a sjednoť dtypes, timezone, sloupce.
- `validate_raw_schema(df, required=...)`: Ověř povinné sloupce a typy (ValueError s detailní zprávou).

### utils/clean.py
- `sanitize(df)`: Sort by `['ticker','date']`, deduplikace, drop řádků s NaN.
- `check_ranges(df)`: Kontrola rozsahu (ceny > 0, volume >= 0, high/low konzistence).
- `adjust_prices_if_needed(df, method="none")`: Volitelné — adjustace (splity/div).

### utils/features.py
- `add_ema(...)`
- `add_residuals_zscore(...)`
- `add_atr(...)`
- `add_hurst(...)`
- `add_ou_halflife(...)`

### utils/events.py (volitelné)
- `add_event_block(...)`: Přidá `event_block=1`, pokud datum spadá do intervalu kolem earnings/dividend.

### utils/signals.py
- `apply_quality_filters(...)`: Vrátí df s `eligible=1`, pokud projde filtry.
- `generate_long_signals(...)`: Přidá `signal_long` a parametry vstupu/výstupu.

### utils/risk.py
- `atr_volatility_sizing(...)`: Velikost pozice podle % risku účtu a ATR.

### core/backtest.py
- `run_vector_backtest(...)`: Vektorový backtest (TP/SL/TIME, concurrency, equity).

### core/eval.py
- `evaluate_trades(...)`: Výpočet WR, PF, avg win/loss, DD, Sharpe, MAR.

---

## 4. Feature definice (formule)

- **EMA:** `ema_t = alpha*price_t + (1-alpha)*ema_{t-1}`, `alpha = 2/(n+1)`
- **Reziduum:** `resid = close - ema_20`
- **Z-score:** `z = resid / stdev(resid, std_window)`
- **ATR:** `ATR = rolling_mean(true_range, n)`; `ATR% = ATR/close`
- **Hurst (R/S):** `E[R(n)/S(n)] ~ C * n^H` → odhad H z log-log regrese
- **OU half-life:** `x_t = a + phi*x_{t-1} + eps_t`; `half_life = -ln(2)/ln(phi)`

---

## 5. Konfigurace (YAML příklad)

```yaml
data:
  raw_paths: ["/ABSOLUTE/OR/RELATIVE/RAW/*.parquet"]
  tz: "UTC"
  adjusted_prices: false

features:
  ema_window: 20
  z_std_window: 20
  atr_window: 14
  hurst_window: 250
  ou_lookback: 60

signals:
  z_entry: -2.5
  z_exit: -0.5
  stop_z: -3.5
  time_stop: 5
  hurst_max: 0.45
  atrp_min: 0.01
  atrp_max: 0.04

risk:
  capital: 100000
  risk_per_trade: 0.01
  max_concurrent: 5

events:
  earnings_path: null
  dividends_path: null
  pre: 1
  post: 1
```

---

## 6. CLI (příklady)

```bash
# End-to-end: raw -> clean -> features -> signals -> (sizing) -> backtest -> eval
python -m trader.cli --config config/config.yml run

# Pouze kontrola a výpočet features
python -m trader.cli features

# Pouze signály s overrides
python -m trader.cli signals --z_entry -2.8 --time_stop 7
```

---

## 7. Dokumentace

- **Docstringy** (NumPy nebo Google style) u všech public funkcí
- **README.md**: rychlý start + datové kontrakty
- Volitelné: **pdoc** nebo **mkdocs**
    - `pdoc trader -o docs/`
    - `mkdocs new .` → `mkdocs.yml` → `mkdocs serve`

---

## 8. Testy — pytest (unit only)

- `tests/fixtures/` — syntetická RAW data (pár tickerů, 30–60 barů)

**Doporučené testy:**
- `test_data_ingest.py` — chybějící sloupce/typy → `ValueError`
- `test_clean.py` — deduplikace, sort, NaN handling, range-check
- `test_features.py` — EMA, Z-score, ATR, Hurst, OU HL (syntetika)
- `test_signals.py` — prahy z_entry/z_exit/stop/time + eligible
- `test_backtest.py` — deterministický scénář (TP/SL/TIME, concurrency)
- `test_eval.py` — WR/PF/DD/Sharpe na umělém trade listu

---

## 9. Milníkové Tasks (v3)

### 1. Ingest & Clean
- [ ] `load_raw`, `validate_raw_schema`, `sanitize`, `check_ranges`
- [ ] `adjust_prices_if_needed`

### 2. Features
- [ ] `add_ema`, `add_residuals_zscore`
- [ ] `add_atr`, `add_hurst`, `add_ou_halflife`
- [ ] `add_event_block` (volitelné)

### 3. Signals & Risk
- [ ] `apply_quality_filters`, `generate_long_signals`
- [ ] `atr_volatility_sizing` (volitelné)

### 4. Backtest & Eval
- [ ] `run_vector_backtest` (TP/SL/TIME, equity/cash, concurrency)
- [ ] `evaluate_trades` + export summary do `reports/`

### 5. CLI & Docs
- [ ] `cli.py` orchestrace (sub-commands: features, signals, backtest, run)
- [ ] Docstringy + README + (volitelně) pdoc/mkdocs

---

Tímhle máš **self-contained pipeline**: převezme syrová data, očistí, spočítá features, vytvoří signály, sizing, backtest a vyhodnocení.  
Fundamenty zůstávají mimo (pouze při výběru universa). V dalších epicích lze přidat např. **Kalman fair-value** nebo **cointegration/pairs**.
