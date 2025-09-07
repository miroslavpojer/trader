# 🟢 Epic 1 — MVP + Backtest (v4, Multi-Pipeline)

Cíl: **plně zdokumentovaná Python orchestrace**, která po uzavření burzy spustí:
1. **Raw Data Pipeline** – načtení, validace a příprava sdíleného datasetu
2. **3 nezávislé strategie pipelines** – Mean Reversion, Trend Following, ETF Rotation
3. **Backtest a vyhodnocení každé strategie zvlášť**
4. **Souhrnný reporting** (výkon, risk, korelace strategií)

---

## 🔹 Pipeline 0: Raw Data (Shared Ingest & Clean)

**Princip:** společný krok pro všechny strategie – stáhne, vyčistí a připraví data.

### Tasks
- [ ] `load_raw(paths, tz="UTC")`: Načti OHLCV za poslední rok (CSV/Parquet)
- [ ] `validate_raw_schema(df, required=...)`: Ověř povinné sloupce a typy
- [ ] `sanitize(df)`: seřazení podle ticker/date, deduplikace, drop NaN
- [ ] `check_ranges(df)`: kontrola cen (ceny > 0, high ≥ low, volume ≥ 0)
- [ ] `adjust_prices_if_needed(method="split")`: volitelné, adjustace při splitech
- [ ] Export do `base_ohlcv.parquet`
- [ ] Připojit `events.parquet` (earnings/div, pokud dostupné)
- [ ] Založit whitelist universa (`universes/*.json`) – fundamentální filtry mimo scope MVP

### Output
- `data_cache/base_ohlcv.parquet`
- `data_cache/events.parquet`
- `universes/universe_main.json`, `universes/universe_etf.json`

---

## 🔹 Pipeline 1: Mean Reversion (Elastic Snapback)

**Princip:** návrat k průměru po krátkodobé odchylce.  
Funguje při nízkém trendu (ADX < 22, Hurst < 0.5). Typický holding 2–5 dní.

### Setup
**BUY:**
- Hurst < 0.45
- Close pod dolní Bollinger (20, 2σ)
- Z-score < –2.0
- RSI(2) < 5
- Stop-loss: swing low –0.7×ATR(14)
- Exit: SMA20 nebo RSI(2) > 70

**SELL:**
- Hurst < 0.45
- Close nad horní Bollinger (20, 2σ)
- Z-score > +2.0
- RSI(2) > 95
- Stop-loss: swing high +0.7×ATR(14)
- Exit: SMA20 nebo RSI(2) < 30

### Tasks
- [ ] `add_ema`, `add_residuals_zscore`, `add_atr`, `add_hurst`, `add_ou_halflife`
- [ ] Generace signálů: `apply_quality_filters`, `generate_long_signals`
- [ ] Risk: `atr_volatility_sizing` (risk_per_trade ≤ 1 %)
- [ ] Backtest: `run_vector_backtest` s TP/SL/TimeStop, equity a trades
- [ ] Eval: `evaluate_trades` → WR, PF, Sharpe, DD, MAR

### Output
- `reports/mr/trades.csv`
- `reports/mr/equity.csv`
- `reports/mr/summary.json`

---

## 🔹 Pipeline 2: Trend Following (SteadyStride)

**Princip:** „trend má tendenci pokračovat déle, než si lidé myslí“.  
Funguje při trendu (ADX > 25, Hurst > 0.5). Typický holding: dny až týdny.

### Setup
**BUY:**
- Proražení rezistence / nové high
- Cena nad SMA50 a SMA200
- Stop-loss: pod swing low nebo SMA50 nebo trailing ATR
- Exit: trailing stop (2×ATR) nebo návrat pod SMA50

**SELL:**
- Proražení supportu / nové low
- Cena pod SMA50 a SMA200
- Stop-loss: nad swing high nebo trailing ATR
- Exit: trailing stop

### Tasks
- [ ] `add_sma`, `add_adx`, `add_atr`
- [ ] Detekce breakoutů (lokální high/low, swing struktura)
- [ ] Signály: trend filter (SMA50>200, ADX > 25) + breakout condition
- [ ] Risk: fixní risk_per_trade ≤ 1 % účtu
- [ ] Backtest: breakout logika s trailing stopem (equity & trades)
- [ ] Eval: CAGR, MAR ratio, max hold time, max DD

### Output
- `reports/tf/trades.csv`
- `reports/tf/equity.csv`
- `reports/tf/summary.json`

---

## 🔹 Pipeline 3: ETF Rotation (QuietFlow)

**Princip:** měsíční rotace mezi ETF podle momenta a volatility.  
Cíl: pokrýt hluchá místa, stabilní low-maintenance vrstva.

### Setup
- **Universe:** velké ETF (SPY, QQQ, IWM, XLK, XLP, XLV, …)
- **Výběr:** top N podle 3–6M momentum, vyřazení ETF s vysokou volatilitou
- **Sizing:** risk parity (inverse vola)
- **Exit:** měsíční rebalance, kill-switch při extrémní volatilitě

### Tasks
- [ ] Výpočet 3M a 6M momentum, 20D volatility, korelací ETF
- [ ] Ranking a výběr top N ETF (configurable)
- [ ] Portfolio vážení: inverse volatility weights, max váha/ETF
- [ ] Risk: max port risk ≤ 20 % kapitálu, per ETF ≤ 5–10 %
- [ ] Backtest: měsíční rebalance loop, equity & trades
- [ ] Eval: Sharpe vs SPY benchmark, tracking error, max DD

### Output
- `reports/etf/trades.csv`
- `reports/etf/equity.csv`
- `reports/etf/summary.json`

---

## 🔹 Orchestrace (CLI)

- `pipeline_raw` – spustí ingest + clean + export cache
- `pipeline_mr` – běží nad `base_ohlcv.parquet`, ukládá do `reports/mr/`
- `pipeline_tf` – běží nad `base_ohlcv.parquet`, ukládá do `reports/tf/`
- `pipeline_etf` – běží nad `base_ohlcv.parquet`, ukládá do `reports/etf/`
- `pipeline_all` – orchestruje všechny nad jedním cache runem

---

## 🔹 Output MVP

- **Per pipeline reports:**
    - `trades.csv`
    - `equity.csv`
    - `summary.json`
- **Souhrnný přehled:**
    - Kombinovaný reporting všech tří strategií
    - Tabulka WR, PF, Sharpe, DD, CAGR, korelace mezi strategiemi

---

Tímto máš MVP, které rovnou validuje **3 rozdílné typy strategií** (Mean Reversion, Trend Following, ETF Rotation) + společnou datovou pipeline.  
Dál lze rozšiřovat o další pipelines (pairs, breakout, panic rebound, seasonality) a navázat Robustností, Adaptací, Automatizací a Portfoliem.
