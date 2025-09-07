# 📊 Pipeline Overview – Long-Only Strategy Suite

Tento dokument popisuje orchestraci a jednotlivé dílčí **pipelines** pro long-only obchodování.  
Cílem je mít více nezávislých vrstev (strategií), které pokrývají různá tržní prostředí a minimalizují “hluchá místa”.

---

# 🧭 Noční orchestrátor (po uzavření burz)

**Kdy:** po uzavření US trhů (např. 22:30–23:00 CET).  
**Cíl:** stáhnout a vyčistit poslední **−1 rok** dat, zvalidovat a připravit sdílené artefakty, pak spustit paralelně dílčí pipelines.

### Fáze 0 – Ingest & Clean (společná)
- Stáhnout OHLCV posledních 365 dní, earnings/dividendy (volitelné)
- Čistka, validace, adjustace
- Cache: `base_ohlcv.parquet`, `events.parquet`
- Universe: whitelist/blacklist z fundamentů (`universes/*.json`)

---

# 🧩 Dílčí pipelines

Každá pipeline:
- Input: `base_ohlcv.parquet` + volitelně `events.parquet` + `universe_*.json`
- Output: `reports/<strategy>/signals_YYYYMMDD.csv`, `trades.csv`, `summary.json`

---

## 1) Elastic Snapback (Main MR)

- **Typ:** Mean reversion na individuálních akciích  
- **Features:** EMA, rezidua, Z-score, ATR, Hurst, OU half-life, event block  
- **Specifičnost / Edge:**  
  - Spojení **reziduální MR** + **režimové filtry** (Hurst, ATR%)  
  - Vysoce selektivní, nízká frekvence → lepší robustnost  
- **Očekávaný výkon:** ~10–20 obchodů/rok, +12–18 % ročně  

---

## 2) TwinTrack Long Legs (MR Pairs)

- **Typ:** Párový obchod, ale pouze long na undervalued leg (no short)  
- **Features:** Spread Z-score, OU half-life, Hurst spreadu  
- **Specifičnost / Edge:**  
  - Použití párové stability, ale risk jen na **long leg**  
  - Diverzifikace mimo single-stock MR  
- **Očekávaný výkon:** +5–10 % ročně, 30–60 obchodů/rok  

---

## 3) SteadyStride (Trend Following Pullback)

- **Typ:** Trend following, long-only pullback do uptrendu  
- **Features:** EMA 50/200, RSI(2), ATR trailing stop  
- **Specifičnost / Edge:**  
  - Kryje trendy režimy, kdy MR selhává  
  - Kupuje **dipy ve směru trendu**  
- **Očekávaný výkon:** ~8–12 % ročně, 20–40 obchodů/rok  

---

## 4) QuietFlow ETF (ETF Rotation)

- **Typ:** ETF long-only rotace (momentum/defenzivní)  
- **Features:** 3–6M momentum, 20D vola, korelace, risk parity sizing  
- **Specifičnost / Edge:**  
  - Nízká údržba, **risk parity** váhy  
  - Pokrytí “hluchých míst” → stabilní long bias  
- **Očekávaný výkon:** ~6–10 % ročně, měsíční rebalance  

---

## 5) Springboard (Breakout Retest Long)

- **Typ:** Trendová breakout/retest strategie  
- **Features:** Swing highs, ATR, objemový filtr  
- **Specifičnost / Edge:**  
  - Zaměřeno na **early stage trendy**  
  - Čistý pattern breakout + retest  
- **Očekávaný výkon:** ~8–12 % ročně, 20–30 obchodů/rok  

---

## 6) RubberBand (Post-Panic Rebound)

- **Typ:** Mean reversion po panice (rychlý swing)  
- **Features:** 1D drop > k×ATR, RSI(2)<5, volume spike, range spike  
- **Specifičnost / Edge:**  
  - Exploituje **short-term paniky** bez earnings risku  
  - Rychlé “snapback” zisky 1–3 dny  
- **Očekávaný výkon:** +3–6 % ročně, 15–25 obchodů/rok  

---

## 7) Almanac Boost (Seasonality/Calendar)

- **Typ:** Kalendářní anomálie (turn-of-month, EOM) na ETF/large caps  
- **Features:** Kalendářní flagy, vola filter, trend filter OFF  
- **Specifičnost / Edge:**  
  - **Behaviorální edge** → “crowd effects” na konci měsíce  
  - Nízká korelace, minimální údržba  
- **Očekávaný výkon:** +2–4 % ročně, 10–20 obchodů/rok  

---

## 8) Climb & Dip (Uptrend Dip Buy)

- **Typ:** Long-only akcie s kvalitním uptrendem, kupování mělkých dipů  
- **Features:** 6M/12M momentum, EMA20/30, earnings filter  
- **Specifičnost / Edge:**  
  - Spojuje **momentum + quality** bias → bezpečnější longy  
  - Pokrytí mid-term růstových fází  
- **Očekávaný výkon:** +6–10 % ročně, 15–25 obchodů/rok  

---

## 9) Channel Kiss (ATR-Channel ETF)

- **Typ:** ETF swing v bočním trhu (dotek spodního ATR kanálu)  
- **Features:** ATR channels, Hurst≈0.5, trend off  
- **Specifičnost / Edge:**  
  - Exploituje **range-bound ETF** (nízká trendovost)  
  - Nízká náročnost, krátké držení  
- **Očekávaný výkon:** +3–6 % ročně, 10–20 obchodů/rok  

---

# 📈 Souhrn očekávaného výkonu

| Pipeline             | Roční výkon | Obchodů/rok | Specifičnost / Edge |
|----------------------|-------------|-------------|---------------------|
| Elastic Snapback     | 12–18 %     | 10–20       | Rezidua + Hurst + ATR filtry |
| TwinTrack Long Legs  | 5–10 %      | 30–60       | Párová stabilita, long leg only |
| SteadyStride         | 8–12 %      | 20–40       | Trend pullback long |
| QuietFlow ETF        | 6–10 %      | ~12         | ETF rotace, risk parity |
| Springboard          | 8–12 %      | 20–30       | Breakout + retest edge |
| RubberBand           | 3–6 %       | 15–25       | Post-panic MR rebound |
| Almanac Boost        | 2–4 %       | 10–20       | Kalendářní anomálie |
| Climb & Dip          | 6–10 %      | 15–25       | Quality momentum dip buy |
| Channel Kiss         | 3–6 %       | 10–20       | ETF range-bound MR |

**Celkové portfolio cíl:** 20–25 % ročně při nízké korelaci a rozumné volatilitě díky diversifikaci.

---

# 🧠 Závěr

- **Elastic Snapback** je hlavní core edge (reziduální mean reversion).  
- **TwinTrack Pairs** přidává jinou dynamiku mean reversion (spread vs. cena).  
- **Trendové a breakout strategie** kryjí období trending trhu.  
- **ETF rotace a kanály** zajišťují stabilní overlay a “cash booster” efekt.  
- **Sezónní a panické edges** přidávají krátkodobé, behaviorální signály.  

Tímto mixem se pokrývají různá prostředí trhu, což zvyšuje šanci na dlouhodobou robustnost a udržení edge.
